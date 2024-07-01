import aiohttp.web
import pytest
import pytest_asyncio
from aiohttp.test_utils import make_mocked_request

from colvert.database import Database
from colvert.ui import setup_app


@pytest_asyncio.fixture(scope="session")
async def sample_db() -> Database:
    db = Database()
    await db.load_files(["./samples/test.csv"])
    return db

@pytest_asyncio.fixture()
async def app() -> aiohttp.web.Application:
    return setup_app()

@pytest.fixture()
def get_request(app) -> aiohttp.web.Request:
    return make_mocked_request("GET", "/", app=app)

@pytest_asyncio.fixture
async def http_server_sample_db(aiohttp_client, sample_db, app) -> aiohttp.web.Application:
    app["db"] = sample_db
    return await aiohttp_client(app)


@pytest_asyncio.fixture
async def http_server(aiohttp_client, sample_db) -> aiohttp.web.Application:
    app = setup_app()
    app["db"] = Database()
    return await aiohttp_client(app)
