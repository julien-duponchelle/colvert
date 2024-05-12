import pytest
import pytest_asyncio
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import Request

from ....database import Database
from ....ui.charts import Line, Pie, Table


class TestCharts:
    @pytest_asyncio.fixture(scope="class")
    async def db(self):
        db = Database()
        await db.load_files(["./samples/test.csv"])
        return db
    
    @pytest.fixture(scope="class")
    def request(self) -> Request:
        return make_mocked_request("GET", "/")
    
    # Pie Chart is use to test the common functionality of the charts
    @pytest.mark.asyncio
    async def test_validate_pie(self, request, db):
        await Pie(request, await db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL"), {}).build()
        with pytest.raises(expected_exception=ValueError, match="2 columns"):
            await Pie(request, await db.sql("SELECT COUNT(*) FROM test"), {}).build()
        with pytest.raises(ValueError, match="NUMBER"):
            await Pie(request, await db.sql("SELECT 'First Name','Last Name' FROM test"), {}).build()
        with pytest.raises(ValueError, match="need max 10 rows"):
            await Pie(request, await db.sql("SELECT 1,'First Name' FROM test"), {}).build()

    @pytest.mark.asyncio
    async def test_validate_table(self, request, db):
        await Table(request, await db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL"), {}).build()
        # Test empty result
        await Table(request, await db.sql("CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR)"), {}).build()

    @pytest.mark.asyncio
    async def test_render_pie_options(self, request, db):
        result = await db.sql("SELECT COUNT(*),'First Name' FROM test")
        response = await Pie(request, result, {"hole": 0.5}).build()
        assert 'plotly-graph-div' in response
        assert '0.5' in response
        assert 'Title' in response

    @pytest.mark.asyncio
    async def test_render_pie(self, request, db):
        result = await db.sql("SELECT COUNT(*),'First Name' FROM test")
        response = await Pie(request, result, {}).build()
    
        assert 'plotly-graph-div' in response

    @pytest.mark.asyncio
    async def test_render_line(self, request, db):
        result = await db.sql("SELECT COUNT(*),'First Name' FROM test")
        response = await Line(request, result, {}).build()
        assert 'plotly-graph-div' in response
