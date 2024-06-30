import pytest
import pytest_asyncio
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import Application, Request

from ....database import Database
from ....ui import setup_app
from ....ui.charts import Line, Pie, Table


@pytest_asyncio.fixture(scope="module")
async def db():
    db = Database()
    await db.load_files(["./samples/test.csv"])
    return db

@pytest.fixture(scope="module")
def app() -> Application:
    return setup_app()

@pytest.fixture(scope="module")
def get(app) -> Request:
    return make_mocked_request("GET", "/", app=app)

# Pie Chart is use to test the common functionality of the charts
@pytest.mark.asyncio
async def test_validate_pie(get, db):
    await Pie(get, await db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL"), {}).build()
    with pytest.raises(expected_exception=ValueError, match="2 columns"):
        await Pie(get, await db.sql("SELECT COUNT(*) FROM test"), {}).build()
    with pytest.raises(ValueError, match="NUMBER"):
        await Pie(get, await db.sql("SELECT 'First Name','Last Name' FROM test"), {}).build()
    with pytest.raises(ValueError, match="need max 10 rows"):
        await Pie(get, await db.sql("SELECT 1,'First Name' FROM test"), {}).build()

@pytest.mark.asyncio
async def test_validate_table(get, db):
    await Table(get, await db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL"), {}).build()
    # Test empty result
    await Table(get, await db.sql("CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR)"), {}).build()

@pytest.mark.asyncio
async def test_render_pie_options(get, db):
    result = await db.sql("SELECT COUNT(*),'First Name' FROM test")
    pie = Pie(get, result, {"hole": 0.5})
    assert pie.user_options == {"hole": 0.5}
    response = await pie.build()
    assert 'plotly-graph-div' in response
    assert '0.5' in response
    assert 'Title' in response

@pytest.mark.asyncio
async def test_render_pie(get, db):
    result = await db.sql("SELECT COUNT(*),'First Name' FROM test")
    response = await Pie(get, result, {}).build()
    assert 'plotly-graph-div' in response

@pytest.mark.asyncio
async def test_render_line(get, db):
    result = await db.sql("SELECT COUNT(*),'First Name' FROM test")
    response = await Line(get, result, {}).build()
    assert 'plotly-graph-div' in response

@pytest.mark.asyncio
async def test_line_user_options(get, db):
    result = await db.sql("SELECT COUNT(*),'First Name' FROM test")
    line = Line(get, result, {'facet_row': None})
    assert line.user_options == {}
    line = Line(get, result, {'facet_row': ''})
    assert line.user_options == {}
    line = Line(get, result, {'facet_row': 'First Name'})
    assert line.user_options == {'facet_row': 'First Name'}


