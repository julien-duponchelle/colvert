import aiohttp.web
import pytest_asyncio

from colvert.database import Database
from colvert.ui import setup_app


@pytest_asyncio.fixture(scope="session")
async def sample_db() -> Database:
    db = Database()
    await db.load_files(["./samples/test.csv"])
    return db


@pytest_asyncio.fixture
async def http_server_sample_db(aiohttp_client, sample_db) -> aiohttp.web.Application:
    app = setup_app()
    app["db"] = sample_db
    return await aiohttp_client(app)


@pytest_asyncio.fixture
async def http_server(aiohttp_client, sample_db) -> aiohttp.web.Application:
    app = setup_app()
    app["db"] = Database()
    return await aiohttp_client(app)
