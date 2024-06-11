import asyncio

# import traceback

# import time
from playwright.async_api import TimeoutError as PlaywriteTimeoutError
from playwright.async_api import async_playwright

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerBackTask, CrawlerContent, DatapoolContentType
from ...utils import canonicalize_url
from ..base_plugin import BasePlugin
from ...worker import WorkerTask


class DefaultPlugin(BasePlugin):
    # def __init__(self, ctx):
    #     super().__init__(ctx)

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        return u.scheme in ("https", "http")

    async def process(self, task: WorkerTask):
        logger.info(f"BasePlugin::process({task.url})")

        if task.content_type in (DatapoolContentType.Image, DatapoolContentType.Video, DatapoolContentType.Audio):
            # simply let worker to download and process content
            yield CrawlerContent(
                type=task.content_type,
                # storage_id=storage_id,
                url=task.url,
            )
            return

        async with async_playwright() as playwright:
            webkit = playwright.chromium
            browser = await webkit.launch()
            viewport_height = 1024
            context = await browser.new_context(viewport={"width": 1920, "height": viewport_height})

            page = await context.new_page()
            await page.goto(str(task.url))

            real_url = page.url
            session_meta = await self.ctx.session.get_meta()
            if not self.get_local_url(real_url, session_meta["url"]):
                logger.info("redirected to different domain")
                return

            url = real_url

            p = BasePlugin.parse_url(url)
            platform_tag = await self.get_platform_tag(p.netloc, page, 3600)

            bodys = page.locator("body")
            body = bodys.nth(0)
            body_text = ""
            n_images = 0
            n_hrefs = 0
            expect_changes = True
            while expect_changes:
                expect_changes = False

                # 1. full body
                # c = await body.get_attribute("content")
                # print(c)
                # h = await body.inner_html()
                # print(h)
                new_text = await body.inner_text()
                # print(t)
                # a. new body contains old body plus more text => replace old with new
                old_text = body_text

                if body_text in new_text:
                    body_text = new_text
                    # b. new body head intersects old body tail => merge them
                    # body  =12345678
                    # new   =     67890
                    # result=1234567890
                else:
                    body_text = BasePlugin.merge_head_tail(body_text, new_text)
                if old_text != body_text:
                    expect_changes = True

                # 2. images
                images = await page.locator("img").all()
                new_n_images = len(images)
                if new_n_images != n_images:
                    expect_changes = True
                while n_images < new_n_images:
                    try:
                        src = await images[n_images].get_attribute("src", timeout=100)
                        n_images += 1

                        logger.info(f"{src=}")
                        if src is None:
                            logger.info("--------------------------------------")
                            outerHTML = await images[n_images - 1].evaluate("el => el.outerHTML")
                            logger.info(f"{outerHTML=}")
                            continue

                        full_local_url = BasePlugin.get_local_url(src, session_meta["url"])
                        if full_local_url:
                            # TODO: getting image from browser works somehow but
                            #   requires image type detection, quality check, crossOrigin understading etc
                            #   So for now let's do not in optimal way
                            # content = await self.download(full_local_url)
                            # getting content from browser page instead of downloading it again
                            # content = await BasePlugin.get_webpage_image_bytes(images[n_images-1])
                            # if content:
                            # TODO: parse copyright_tag_id somehow?

                            yield CrawlerContent(
                                platform_tag_id=str(platform_tag) if platform_tag is not None else None,
                                platform_tag_keepout=(platform_tag.is_keepout() if platform_tag is not None else None),
                                type=DatapoolContentType.Image,
                                # storage_id=storage_id,
                                url=full_local_url,
                            )
                        else:
                            logger.info(f'non local: {src=} {session_meta["url"]=}')

                    except PlaywriteTimeoutError:
                        # element may be not ready yet, no problems, will get it on the next iteration
                        # logger.info( 'get_attribute timeout' )
                        expect_changes = True
                        break

                # 3. hrefs
                hrefs = await page.locator("a").all()
                new_n_hrefs = len(hrefs)
                if new_n_hrefs != n_hrefs:
                    expect_changes = True
                while n_hrefs < new_n_hrefs:
                    try:
                        href = await hrefs[n_hrefs].get_attribute("href", timeout=100)
                        n_hrefs += 1
                        if href is None:
                            continue

                        full_local_url = BasePlugin.get_local_url(href, session_meta["url"])
                        if full_local_url:
                            # strict constraint on urls, else may get endless recursions etc
                            full_local_url = canonicalize_url(full_local_url)
                            logger.info(full_local_url)

                            # logger.info( f'---------yielding {video_url=}')
                            yield CrawlerBackTask(url=full_local_url)
                            # logger.info( f'---------yielded {video_url=}')
                        else:
                            logger.info(f'non local: {href=} {session_meta["url"]=}')

                    except PlaywriteTimeoutError:
                        # element may be not ready yet, no problems, will get it on the next iteration
                        # logger.info( 'get_attribute timeout' )
                        expect_changes = True
                        break

                scroll_height1 = await page.evaluate("document.body.scrollHeight")
                await page.mouse.wheel(0, viewport_height * 0.8)
                scroll_height2 = await page.evaluate("document.body.scrollHeight")
                logger.info(f"*********** {scroll_height1=} {scroll_height2=} ****************")
                if scroll_height1 != scroll_height2:
                    expect_changes = True

                await asyncio.sleep(1)
                # await page.screenshot(path=f'/home/psu/page.png')

            # await page.screenshot(path='/home/psu/bottom.png')
            # print('done')
            # print( f'{n_images=}')
            # print( f'{n_hrefs=}')
