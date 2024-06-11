import asyncio

# import importlib
# import inspect
import os

# import sys
import traceback

# from enum import Enum
from typing import List, Optional

from ..common.backend_api import BackendAPI, BackendAPIException
from ..common.logger import logger
from ..common.queues import GenericQueue, QueueMessage, QueueMessageType, QueueRole, QueueTopicMessage
from ..common.session_manager import SessionManager, Session
from ..common.stoppable import Stoppable
from ..common.storage.file_storage import FileStorage
from ..common.types import BaseProducerSettings, InvalidUsageException
from ..worker.utils import get_storage_invalidation_topic
from ..worker.worker import WorkerFileStorage

# from .rules import DatapoolRulesChecker


class BaseProducer(Stoppable):
    def __init__(self, cfg: Optional[BaseProducerSettings] = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else BaseProducerSettings()
        self.session_manager = SessionManager(self.cfg.REDIS_HOST, self.cfg.REDIS_PORT)

        if not self.cfg.CLI_MODE:
            self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)

        # receives tasks from workers
        self.eval_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.EVAL_TASKS_QUEUE_NAME,
        )
        logger.info("created receiver eval_tasks")

        # will invalidate worker cache entries
        self.topics_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.TOPICS_QUEUE_NAME,
            topic=True,  # for Rabbitmq publisher
        )
        logger.info("created publisher worker_tasks")
        if self.cfg.CLI_MODE is True:
            self.stop_task_received = asyncio.Event()

        # self.datapool_rules_checker = DatapoolRulesChecker()

    def run(self):
        self.tasks.append(asyncio.create_task(self.router_loop()))
        self.eval_queue.run()
        self.topics_queue.run()
        super().run()

    async def wait(self):
        if self.cfg.CLI_MODE is False:
            logger.error("baseproducer invalid usage")
            raise InvalidUsageException("not a cli mode")

        logger.info("BaseProducer wait()")
        await self.stop_task_received.wait()
        logger.info("BaseProducer stop_task_received")
        waiters = (
            self.eval_queue.until_empty(),
            self.topics_queue.until_empty(),
        )
        await asyncio.gather(*waiters)
        logger.info("BaseProducer wait done")

    async def stop(self):
        await self.eval_queue.stop()
        await self.topics_queue.stop()
        await super().stop()
        logger.info("BaseProducer stopped")

    async def router_loop(self):
        try:
            while not await self.is_stopped():
                message = await self.eval_queue.pop(timeout=1)
                if message:
                    qm = QueueMessage.decode(message.body)
                    logger.info(f"{qm.session_id=}")
                    try:
                        session = await self.session_manager.get(qm.session_id)
                        if session is None or not await session.is_alive():
                            logger.info(f"session is deleted or stopped {qm.session_id=} {message.message_id}")
                            await self.eval_queue.mark_done(message)
                            continue

                        if qm.type == QueueMessageType.Task:
                            task = qm.data
                            logger.info(f"Producer got: {task}")

                            worker_storage = WorkerFileStorage(self.cfg.WORKER_STORAGE_PATH, task["worker_id"])
                            with worker_storage.get_reader(task["storage_id"]) as raw_data_reader:
                                await self.process_content(session, raw_data_reader, task)

                            if not self.is_shared_storage():
                                # tell worker that his storage item can be removed
                                await self.topics_queue.push(
                                    QueueTopicMessage(
                                        get_storage_invalidation_topic(task["worker_id"]),
                                        {"storage_id": task["storage_id"]},
                                    )
                                )
                        elif qm.type == QueueMessageType.Stop:
                            logger.info("base_producer: stop task received")
                            self.stop_task_received.set()
                        else:
                            raise Exception(f"!!!!!!!!!!!!!!! BUG: unexpected {message=} {qm=}")

                        await self.eval_queue.mark_done(message)
                    except BackendAPIException as e:
                        logger.error("Catched BackendAPIException")
                        logger.error(traceback.format_exc())
                        await self.eval_queue.reject(message)
                        await asyncio.sleep(5)
                    except Exception as e:
                        logger.error("Catched Exception")
                        logger.error(traceback.format_exc())
                        await self.eval_queue.reject(message, requeue=False)

        except Exception as e:
            logger.error(f"Catched: {traceback.format_exc()}")
            logger.error(f"!!!!!!! Exception in Datapools::router_loop() {e}")

    async def process_content(self, session: Session, raw_data, task):
        logger.info(f"BaseProducer::process_content {type(raw_data)=}")
        # path = os.path.join(self.cfg.STORAGE_PATH, str(datapool_id))
        if not self.is_shared_storage():
            path = self.cfg.STORAGE_PATH
            if not os.path.exists(path):  # type: ignore
                os.mkdir(path)  # type: ignore
            storage = FileStorage(path)
            # put data into persistent storage
            await storage.put(task["storage_id"], raw_data)

        if await session.is_alive():  # session may have been stopped/deleted while processing content
            await session.inc_evaluated_content()

    def is_shared_storage(self):
        return self.cfg.STORAGE_PATH is None or self.cfg.WORKER_STORAGE_PATH == self.cfg.STORAGE_PATH
