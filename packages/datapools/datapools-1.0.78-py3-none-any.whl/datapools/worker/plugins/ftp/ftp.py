import io
import time

import asyncio
import os
from ftplib import FTP_PORT
import aioftp

from typing import List, Optional, Callable

# import httpx

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerContent, TryLater
from ..base_plugin import BasePlugin, BaseTag, BaseReader, ConnectionFailed, AuthFailed, ReadFailed
from ...worker import WorkerTask


class FTPReader(BaseReader):
    filepath: str
    filesize: int
    host: str
    port: int
    user: str
    passwd: str

    def __init__(self, host, port, user, passwd, filepath, filesize):
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

        # filepath = "/Paintings of the World 3(13 min).mp4"
        # filesize = 461417090

        self.filepath = filepath
        self.filesize = int(filesize)

    async def read_to(self, f: io.IOBase, stopper: Callable):
        total = 0
        i = 0
        is_stopped = False
        done = True
        try:
            client = aioftp.Client(socket_timeout=10, connection_timeout=10, path_timeout=10)
            try:
                await client.connect(self.host, self.port)
            except asyncio.TimeoutError as e:
                raise ConnectionFailed() from e

            try:
                await client.login(self.user, self.passwd)
            except aioftp.errors.StatusCodeError as e:
                logger.error("Failed login")
                raise AuthFailed() from e

            stream = await client.download_stream(self.filepath)
            async for block in stream.iter_by_block():
                if not block:
                    break
                # async for block in stream.iter_by_block():

                # logger.info(f"{type(block)=} {len(block)=}")

                f.write(block)
                # logger.info("wrote")
                total += len(block)

                if int(total / self.filesize * 100) >= i * 10:
                    # if True:
                    logger.info(f"FTP read total {total} vs {self.filesize} ({int(total/self.filesize*100)}%)")
                    i += 1

                if total >= self.filesize:
                    done = True
                    break
                if await stopper():
                    logger.info("aborting")
                    # await self.client.abort()
                    # stream.close()
                    # is_stopped = True
                    break
                # else:
                # await stream.finish()

            logger.info(f"FTP read done, {total=} ({int(total/self.filesize*100)}%)")
        except aioftp.errors.StatusCodeError:
            logger.info("exception")
            if not is_stopped:
                raise
        except ConnectionResetError:
            logger.info("ConnectionResetError")
            if not done:
                raise


class FTPPlugin(BasePlugin):
    client: aioftp.Client = None
    copyright_tags: List[BaseTag]
    host: str = ""
    port: int = 0
    user: str = ""
    passwd: str = ""

    def __init__(self, ctx, demo_tag=None):
        super().__init__(ctx)
        self.copyright_tags = []
        if demo_tag:
            self.copyright_tags.append(BaseTag(demo_tag))

    @staticmethod
    def is_supported(url):
        p = BasePlugin.parse_url(url)
        return p.scheme == "ftp"

    @staticmethod
    def parse_ftp_url(url):
        user = "anonymous"
        passwd = ""
        host = ""
        port = int(FTP_PORT)

        p = BasePlugin.parse_url(url)
        netloc = p.netloc
        p = netloc.split("@")
        if len(p) == 1:  # host[:port] only
            p = netloc.split(":")
            host = p[0]
            if len(p) == 2:
                port = int(p[1])
        else:
            # user:passwd
            u = p[0].split(":")
            user = u[0]
            if len(u) == 2:
                passwd = u[1]

            # host[:port]
            p = p[1].split(":")
            host = p[0]
            if len(p) == 2:
                port = int(p[1])
        return (user, passwd, host, port)

    # async def keepalive(self):
    #     last_noop = 0
    #     while self.client:
    #         now = time.time()
    #         if now - last_noop > 10:
    #             logger.info("NOOP")
    #             await self.client.command("NOOP")
    #             last_noop = now

    async def process(self, task: WorkerTask):
        # requires FULL url ( with credentials )
        (user, passwd, host, port) = self.parse_ftp_url(task.url)
        self.client = aioftp.Client(socket_timeout=10, connection_timeout=10, path_timeout=10)
        try:
            await self.client.connect(host, port)
        except asyncio.TimeoutError:
            yield TryLater()
            return

        try:
            await self.client.login(user, passwd)
        except aioftp.errors.StatusCodeError:
            logger.error("Failed login")
            return

        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

        # asyncio.create_task(self.keepalive())
        # self.ftp.connect(host, port, timeout=10)
        # logger.info(f"{user=} {passwd=}")
        # self.ftp.login(user, passwd)
        # except TimeoutError:
        #     logger.error("connection timeout")
        #     yield TryLater()
        #     return
        # except error_perm:
        #     logger.error("failed login")
        #     return
        # pwd = self.ftp.pwd()
        logger.info("get_curr_dir")

        pwd = await self.client.get_current_directory()
        logger.info(pwd)
        async for x in self._scan_dir(pwd, 0):
            yield x
        self.client = None
        # del self.ftp

    async def _scan_dir(self, path, rec):
        # logger.info(f"scanning {path}")
        # lister = DirectoryListing()
        # self.ftp.dir(path, lister)
        dir_list = await self.client.list(path)
        logger.info(dir_list)

        local_copyright_tag = await self._try_find_license(dir_list)
        if len(self.copyright_tags) == 0:
            logger.info(f"no copyright tag in {path}")
            return
        copyright_tag = self.copyright_tags[-1]

        # copyright_tag is pushed to self.copyright_tags

        for item in dir_list:
            filepath = str(item[0])
            logger.info(
                "\t" * rec
                + item[1]["type"]
                + "\t"
                + filepath
                + "\t"
                + (item[1]["size"] if item[1]["type"] == "file" else "")
            )
            if item[1]["type"] == "dir":
                async for x in self._scan_dir(filepath, rec + 1):
                    yield x
            elif item[1]["type"] == "file":
                filename = os.path.split(filepath)[-1]
                if filename == BasePlugin.license_filename:
                    continue

                yield CrawlerContent(
                    # tag_id=str(tag) if tag is not None else None,
                    # tag_keepout=tag.is_keepout() if tag is not None else None,
                    copyright_tag_id=str(copyright_tag),
                    copyright_tag_keepout=copyright_tag.is_keepout(),
                    # type=content_type,
                    url=filepath,
                    # content=content,
                    content=FTPReader(self.host, self.port, self.user, self.passwd, filepath, item[1]["size"]),
                )
            else:
                raise Exception(f"unknown type of {str(item[0])} - {item[1]['type']}")
        if local_copyright_tag:
            self.copyright_tags.pop()

    async def _try_find_license(self, dir_contents) -> Optional[BaseTag]:
        for item in dir_contents:
            file_path = item[0]
            filename = os.path.split(file_path)[-1]
            # logger.info(path_parts)

            if filename == BasePlugin.license_filename and item[1]["type"] == "file":
                logger.info(f"found {BasePlugin.license_filename}")
                content = await self.download(file_path)
                if content:
                    logger.info(f"got license content: {content=}")
                    tag = await BasePlugin.parse_tag_in(content.decode())
                    # logger.info(f"{tag_id=}")
                    logger.info(f"{tag=}")
                    if tag:
                        self.copyright_tags.append(tag)
                        return tag
        return None

    async def download(self, path):
        res = b""
        async with self.client.download_stream(path) as stream:
            async for block in stream.iter_by_block():
                res += block
        return res
