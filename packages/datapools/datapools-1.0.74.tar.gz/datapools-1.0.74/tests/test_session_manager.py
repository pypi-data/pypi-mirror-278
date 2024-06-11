import asyncio
import pytest
from pytest import fixture

from datapools.common.session_manager import Session, SessionManager, SessionStatus
from datapools.common.types import WorkerSettings, CrawlerHintURLStatus


# @pytest.fixture(scope="session")
# async def asyncio_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield
#     loop.close()


@fixture()
def worker_settings():
    return WorkerSettings()


@fixture()
async def session_manager(worker_settings) -> SessionManager:
    res = SessionManager(worker_settings.REDIS_HOST)
    yield res
    await res.stop()


@fixture()
async def session(session_manager):
    res = await session_manager.create(1)
    yield res
    await session_manager.remove(res.id)


@pytest.mark.anyio
async def test_session_status(session):
    assert await session.get_last_reported_status() is None

    await session.set_last_reported_status(CrawlerHintURLStatus.Success)
    assert await session.get_last_reported_status() == CrawlerHintURLStatus.Success
