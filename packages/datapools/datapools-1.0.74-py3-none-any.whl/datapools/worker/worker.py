import asyncio
import time
import importlib
import tempfile
import inspect
import os
import re
import sys

import traceback
import uuid
from copy import deepcopy
from typing import Optional, Set, List, Tuple, Any, Dict, NamedTuple

from ..common.backend_api import BackendAPI
from ..common.logger import logger
from ..common.queues import GenericQueue, QueueMessage, QueueMessageType, QueueRole, QueueTopicMessage
from ..common.session_manager import SessionManager, Session
from ..common.stoppable import Stoppable
from ..common.storage import FileStorage
from ..common.types import (
    CrawlerBackTask,
    CrawlerContent,
    CrawlerDemoUser,
    TryLater,
    CrawlerHintURLStatus,
    CrawlerNop,
    DatapoolContentType,
    InvalidUsageException,
    WorkerSettings,
)
from .types import WorkerContext, WorkerTask
from .plugins.base_plugin import BasePlugin, UnexpectedContentTypeException, BaseReader, BaseReaderException
from .utils import get_storage_invalidation_topic


class WorkerFileStorage(FileStorage):
    def __init__(self, dstpath, worker_id):
        super().__init__(os.path.join(dstpath, worker_id))


class PluginData(NamedTuple):
    cls: Tuple[str, Any]
    objs: List[BasePlugin] = []
    params: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None


MAX_INSTANCES_ERROR = -1


class CrawlerWorker(Stoppable):
    demo_users: dict[str, dict[str, str]]
    plugins: List[PluginData]

    def __init__(self, cfg: Optional[WorkerSettings] = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else WorkerSettings()
        self.id = uuid.uuid4().hex
        logger.info(f"worker id={self.id}")

        self.demo_users = {}
        self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)

        self.session_manager = SessionManager(self.cfg.REDIS_HOST, self.cfg.REDIS_PORT)

        # Worker storage must be separated from other workers
        # so default schema when path is $STORAGE_PATH/$storage_id does not work here.
        # Using $STORAGE_PATH/$worker_id/$storage_id path
        self.storage = WorkerFileStorage(self.cfg.STORAGE_PATH, self.id)

        self.todo_tasks: Set[asyncio.Task] = set()

        self.init_plugins()
        self.todo_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.WORKER_TASKS_QUEUE_NAME,
            size=self.cfg.TODO_QUEUE_SIZE,
        )
        logger.info("created receiver worker_tasks")
        self.reports_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.WORKER_REPORTS_QUEUE_NAME,
        )
        logger.info("created publisher reports")
        self.producer_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.EVAL_TASKS_QUEUE_NAME,
        )
        logger.info("created publisher eval_tasks")
        self.topics_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.TOPICS_QUEUE_NAME,
            topic=get_storage_invalidation_topic(self.id),
        )
        logger.info("created receiver topics")

        if self.cfg.CLI_MODE is True:
            self.stop_task_received = asyncio.Event()

    def run(self):
        # self.tasks.append( asyncio.create_task( self.tasks_fetcher_loop() ) )
        self.todo_queue.run()
        self.reports_queue.run()
        self.producer_queue.run()
        self.topics_queue.run()
        self.tasks.append(asyncio.create_task(self.worker_loop()))
        self.tasks.append(asyncio.create_task(self.topics_loop()))
        super().run()

    async def wait(self):
        """for CLI mode usage only"""
        if self.cfg.CLI_MODE is False:
            logger.error("worker invalid usage")
            raise InvalidUsageException("not a cli mode")
        logger.info("CrawlerWorker wait()")
        await self.stop_task_received.wait()
        logger.info("CrawlerWorker stop_task_received")
        waiters = (
            self.todo_queue.until_empty(),
            self.reports_queue.until_empty(),
            self.producer_queue.until_empty(),
            self.topics_queue.until_empty(),
        )
        await asyncio.gather(*waiters)
        logger.info("CrawlerWorker wait done")

    async def stop(self):
        await super().stop()
        if len(self.todo_tasks) > 0:
            await asyncio.wait(self.todo_tasks, return_when=asyncio.ALL_COMPLETED)
        await self.todo_queue.stop()
        await self.reports_queue.stop()
        await self.producer_queue.stop()
        await self.topics_queue.stop()

        # for plugin_data in self.plugins:
        #     if plugin_data[0] is not None:
        #         logger.info( f'clearing plugin {plugin_data[1]}')
        #         plugin_data[0] = None
        #         plugin_data[1] = None

        logger.info("worker stopped")

    def init_plugins(self):
        self.plugins = []
        plugin_names = []

        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
        logger.info(f"{plugins_dir=}")

        internal_plugins = []
        for dir_name in os.listdir(plugins_dir):
            if dir_name != "__pycache__" and os.path.isdir(os.path.join(plugins_dir, dir_name)):
                internal_plugins.append(dir_name)
                if self.cfg.USE_ONLY_PLUGINS is None or dir_name in self.cfg.USE_ONLY_PLUGINS:
                    name = f"datapools.worker.plugins.{dir_name}"
                    plugin_names.append(name)

        if self.cfg.ADDITIONAL_PLUGINS is not None:
            for name in self.cfg.ADDITIONAL_PLUGINS:
                if importlib.util.find_spec(name):
                    plugin_names.append(name)

        for name in plugin_names:
            if name not in sys.modules:
                logger.info(f"loading module {name}")
                module = importlib.import_module(name)
            else:
                logger.info(f"RE-loading module {name}")
                module = importlib.reload(sys.modules[name])

            clsmembers = inspect.getmembers(module, inspect.isclass)
            # logger.info( f'{clsmembers=}')

            for cls in clsmembers:
                for base in cls[1].__bases__:
                    # logger.info( f'{base=}')
                    if base.__name__ == "BasePlugin":
                        # logger.info( f'valid plugin class {cls[1]}')
                        (params, config) = self._get_plugin_config_entry(cls[0])
                        self.plugins.append(PluginData(cls=cls, params=params, config=config))
                        break
        # logger.info( f'AFTER:{sys.modules=}')

    async def topics_loop(self):
        # from Producer.Evaluator - receives storage_id which content can be removed
        try:
            while not await self.is_stopped():
                message = await self.topics_queue.pop(timeout=1)
                if message:
                    qm = QueueTopicMessage.decode(message.routing_key, message.body)
                    expected_routing_key = get_storage_invalidation_topic(self.id)
                    if message.routing_key == expected_routing_key:
                        logger.info(f"invalidating storage {qm.data[ 'storage_id' ]}")
                        await self.storage.remove(qm.data["storage_id"])

                        await self.topics_queue.mark_done(message)
                    else:
                        logger.error(f"!!!!!!!!!!!!!!! BUG: unexpected topic {message=} {qm=} {expected_routing_key=}")
                        await self.topics_queue.reject(message, requeue=False)
        except Exception as e:
            logger.error(f"!!!!!!!!Exception in topics_loop() {e}")
            logger.error(traceback.format_exc())

    async def worker_loop(self):
        # fetches urls one by one from the queue and scans them using available plugins
        try:
            while not await self.is_stopped():
                message = await self.todo_queue.pop(timeout=1)
                if message:
                    task = asyncio.create_task(self._process_todo_message(message))
                    self.todo_tasks.add(task)
                    task.add_done_callback(self.todo_tasks.discard)

        except Exception as e:
            logger.error(f"!!!!!!!!Exception in worker_loop() {e}")
            logger.error(traceback.format_exc())

    async def _process_todo_message(self, message):
        qm = QueueMessage.decode(message.body)

        session = await self.session_manager.get(qm.session_id)
        if not session:
            logger.error(f"Session not found {qm.session_id}")
            await self.todo_queue.reject(message, requeue=False)
            return

        if qm.type == QueueMessageType.Task:
            done = False

            task = WorkerTask(url=qm.data["url"], content_type=qm.data.get("content_type"))
            logger.info(f"got {task=} {qm.session_id=}")

            logger.info(f"processing {task.url=}")

            plugin = self._get_url_plugin(task, session)
            logger.info(f"suitable {plugin=}")

            if plugin is None:
                await self.todo_queue.reject(message, requeue=False)
                return

            if plugin == MAX_INSTANCES_ERROR:
                # requeue to the end of queue
                await self.todo_queue.mark_done(message)
                await self._add_back_task(qm.session_id, CrawlerBackTask(url=task.url))

            is_stopped = False
            for attempt in range(0, self.cfg.ATTEMPTS_PER_URL):
                if attempt > 0:
                    logger.info(f"{attempt=}")

                try:

                    if not await session.is_alive():
                        is_stopped = True
                        logger.info(f"Session is stopped, breaking. {qm.session_id=}")
                        break

                    is_postponed = False
                    async for process_res in plugin.process(task):
                        # logger.info( f'{type( process_res )=}')
                        t = type(process_res)
                        # logger.info( f'{(t is CrawlerNop)=}')

                        if not await session.is_alive():
                            is_stopped = True
                            logger.info(f"Session is stopped/deleted, breaking. {qm.session_id=}")
                            break

                        if t is CrawlerContent:
                            await self._process_crawled_content(process_res, session, plugin, task)
                        elif t is CrawlerBackTask:
                            await self._add_back_task(qm.session_id, process_res)
                        elif t is CrawlerDemoUser:
                            ct: CrawlerDemoUser = process_res
                            if ct.platform not in self.demo_users:
                                self.demo_users[ct.platform] = {}
                            if ct.user_name not in self.demo_users[ct.platform]:
                                logger.info(f"============= {dict(ct)} ===========")
                                await self.api.add_demo_user(dict(ct))
                                self.demo_users[ct.platform][ct.user_name] = ct.short_tag_id
                        elif t is TryLater:
                            await session.postpone()
                            is_postponed = True
                            break
                        elif t is CrawlerNop:
                            pass
                        else:
                            raise Exception(f"unknown {process_res=}")

                        await self._notify_process_iteration(qm.session_id)

                        is_stopped = await self.is_stopped()
                        if is_stopped:
                            break

                    logger.info("plugin.process done")
                    if is_postponed is False:
                        await self._set_task_status(
                            qm.session_id,
                            task,
                            CrawlerHintURLStatus.Success if not is_stopped else CrawlerHintURLStatus.Canceled,
                        )

                    done = True
                    break
                except Exception as e:
                    logger.error(f"failed get url: {e}")
                    logger.error(traceback.format_exc())
                    await asyncio.sleep(self.cfg.ATTEMPTS_DELAY)
                if done:
                    break

            plugin.is_busy = False

            if done:
                logger.info(f"sending ack for {message.message_id=}")
                await self.todo_queue.mark_done(message)
            else:
                logger.info(f"sending reject for {message.message_id=}")
                await self.todo_queue.reject(message, requeue=False)
                await self._set_task_status(qm.session_id, task, CrawlerHintURLStatus.Failure)

        elif qm.type == QueueMessageType.Stop:
            await self.todo_queue.mark_done(message)
            logger.info("worker: got stop task")

            await self.producer_queue.push(QueueMessage(qm.session_id, QueueMessageType.Stop))
            # notifying scheduler that we are done
            await self.reports_queue.push(QueueMessage(qm.session_id, QueueMessageType.Stop))
            self.stop_task_received.set()

        else:
            logger.error(f"!!!!!!!!!!!!!!! BUG: unexpected {message=} {qm=}")
            await self.todo_queue.reject(message)

    async def _set_task_status(self, session_id, task, status: CrawlerHintURLStatus):
        await self.reports_queue.push(
            QueueMessage(session_id, QueueMessageType.Report, {"task": deepcopy(task), "status": status.value})
        )

    async def _notify_process_iteration(self, session_id):
        await self.reports_queue.push(QueueMessage(session_id, QueueMessageType.ProcessIteration))

    async def _process_crawled_content(
        self, cc: CrawlerContent, session: Session, plugin: BasePlugin, task: WorkerTask
    ):
        no_tagged_content = True
        if not await session.has_content(cc.url):

            async def process_content():
                nonlocal no_tagged_content
                logger.info(f"process_content {type(cc.content)=}")
                if cc.content:
                    if not cc.type:
                        try:
                            cc.type = BasePlugin.get_content_type_by_content(cc.content)
                        except UnexpectedContentTypeException:
                            logger.error("Unsupported content, skipped")

                    logger.info(f"{cc.type=}")

                    if cc.type:
                        if not cc.tag_id:
                            # trying to parse author tag
                            if cc.type == DatapoolContentType.Image:
                                image_tag = BasePlugin.parse_image_tag(cc.content)
                                cc.tag_id = str(image_tag) if image_tag is not None else None
                                cc.tag_keepout = image_tag.is_keepout() if image_tag is not None else False
                            # TODO: add video/audio parsing here

                        if cc.tag_id is not None or cc.copyright_tag_id is not None or cc.platform_tag_id is not None:
                            no_tagged_content = False

                            storage_id = self.storage.gen_id(cc.url)
                            logger.info(f"putting to {storage_id=}")
                            await self.storage.put(storage_id, cc.content)

                            await session.add_content(cc.url)
                            await session.inc_crawled_content()

                            if cc.tag_id is not None:
                                await session.inc_tag_usage(cc.tag_id, cc.tag_keepout)
                            if cc.copyright_tag_id is not None:
                                await session.inc_tag_usage(cc.copyright_tag_id, cc.copyright_tag_keepout)
                            if cc.platform_tag_id is not None:
                                await session.inc_tag_usage(cc.platform_tag_id, cc.platform_tag_keepout)

                            # notifying producer about new crawled data
                            await self.producer_queue.push(
                                QueueMessage(
                                    session.id,
                                    QueueMessageType.Task,
                                    {
                                        "parent_url": task.url,
                                        "url": cc.url,
                                        "storage_id": storage_id,
                                        "tag_id": cc.tag_id,
                                        "tag_keepout": cc.tag_keepout,
                                        "copyright_tag_id": cc.copyright_tag_id,
                                        "copyright_tag_keepout": cc.copyright_tag_keepout,
                                        "platform_tag_id": cc.platform_tag_id,
                                        "platform_tag_keepout": cc.platform_tag_keepout,
                                        "type": DatapoolContentType(cc.type).value,
                                        "priority_timestamp": cc.priority_timestamp,
                                        "worker_id": self.id,
                                    },
                                )
                            )
                        else:
                            logger.info("no tag available")
                    else:
                        logger.info("unknown content type")
                else:
                    logger.info("no content")

            last_check = 0
            is_stopped = False
            content_ok = True

            async def stopper():
                nonlocal is_stopped
                if time.time() - last_check > 1:
                    is_stopped = await self.is_stopped() or not await session.is_alive()
                    return is_stopped
                return False

            if not cc.content:
                logger.info("no content, downloading from url")
                with tempfile.TemporaryFile("wb+") as tmp:
                    try:
                        async for chunk in plugin.async_read_url(cc.url, expected_type=cc.type):
                            tmp.write(chunk)
                            if await stopper():
                                is_stopped = True
                                break
                        cc.content = tmp
                    except UnexpectedContentTypeException as e:
                        logger.error(f"Unexpected content type: {str(e)}")
                        content_ok = False
                    if content_ok and not is_stopped:
                        await process_content()

            elif isinstance(cc.content, BaseReader):
                logger.info("content is BaseReader instance")

                with tempfile.TemporaryFile("wb+") as tmp:
                    logger.info("read_to tmp")
                    try:
                        await cc.content.read_to(tmp, stopper)
                        logger.info("read_to done")
                    except BaseReaderException as e:
                        logger.error("Reader failure: {e}")
                        content_ok = False

                    if content_ok and not is_stopped:
                        cc.content = tmp
                        await process_content()
            else:
                await process_content()

        else:
            logger.info(f"content url exists {cc.url}")

        # Stats for scheduler decision whether to continue crawling or not
        if no_tagged_content:
            logger.info("inc_since_last_tagged")
            await session.inc_since_last_tagged()
        else:
            logger.info("reset_since_last_tagged")
            await session.reset_since_last_tagged()
        # n = await session.get_since_last_tagged()
        # logger.info(f"get_since_last_tagged: {n}")

    async def _add_back_task(self, session_id, task: CrawlerBackTask):
        await self.reports_queue.push(QueueMessage(session_id, QueueMessageType.Task, task.to_dict()))

    def _get_plugin_object(self, cls, session: Session) -> BasePlugin:
        ctx = WorkerContext(session=session)  # type: ignore

        args = [ctx]
        kwargs = {}
        logger.info(f"_get_plugin_object {cls=}")

        # convert class name into config plugins key
        # example: GoogleDrivePlugin => google_drive
        # example: S3Plugin => s3
        (params, __config) = self._get_plugin_config_entry(cls[0])
        if params is not None:
            # plugin config dict keys must match plugin's class __init__ arguments
            kwargs = params

        return cls[1](*args, **kwargs)

    def _get_plugin_config_entry(self, cls_name):
        cap_words = re.sub(r"([A-Z])", r" \1", cls_name).split()
        # logger.info(f'{cap_words=}')
        config_key = "_".join(list(map(lambda x: x.lower(), cap_words[:-1])))
        # logger.info(f'{config_key=}')
        config_entry = self.cfg.plugins_config.get(config_key)
        if config_entry is not None:
            logger.info(config_entry)
            params = {k: v for k, v in config_entry.items() if k != "config"}
            config = config_entry.get("config")
            return (params, config)
        return (None, None)

    def _get_url_plugin(self, task: WorkerTask, session: Session):

        def get_free_obj(plugin_data: PluginData):
            for obj in plugin_data.objs:
                if not obj.is_busy:
                    return obj
            return None

        for plugin_data in self.plugins:
            if plugin_data.cls[0] != "DefaultPlugin":
                if plugin_data.cls[1].is_supported(task.url):

                    max_instances = None
                    if plugin_data.config is not None:
                        max_instances = plugin_data.config.get("max_instances")

                    obj = get_free_obj(plugin_data)
                    if obj is None:
                        if max_instances is not None:
                            busy_count = plugin_data.cls[1].get_busy_count()
                            if busy_count >= max_instances:
                                logger.info(f"max instances reached, {max_instances=}")
                                return MAX_INSTANCES_ERROR

                        obj = self._get_plugin_object(plugin_data.cls, session)
                        obj.is_busy = True
                        plugin_data.objs.append(obj)
                    else:
                        obj.is_busy = True
                    return obj

        # creating/using existing default plugin
        for plugin_data in self.plugins:
            if plugin_data.cls[0] == "DefaultPlugin":
                if plugin_data.cls[1].is_supported(task.url):
                    obj = get_free_obj(plugin_data)
                    if obj is None:
                        if max_instances is not None and plugin_data.cls[1].busy_count >= max_instances:
                            return MAX_INSTANCES_ERROR

                        obj = self._get_plugin_object(plugin_data.cls, session)
                        obj.is_busy = True
                        plugin_data.objs.append(obj)
                    else:
                        obj.is_busy = True
                    return obj
