import pytest
from aiohttp.web import Request

from ...database import Database
from ...ui.charts import Line, Pie
from ...ui.charts.base import OptionTypeFloat, OptionTypeString


class TestCharts:
    @pytest.fixture(scope="class")
    def db(self):
        db = Database()
        db.load_file("./samples/test.csv")
        return db
    
    def request(self) -> Request:
        return Request()
    
    @pytest.mark.asyncio
    async def test_validate_pie(self, request, db):
        await Pie(request, db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL")).build()
        with pytest.raises(ValueError, match="2 columns"):
            await Pie(request, db.sql("SELECT COUNT(*) FROM test")).build()
        with pytest.raises(ValueError, match="NUMBER"):
            await Pie(request, db.sql("SELECT 'First Name','Last Name' FROM test")).build()
        with pytest.raises(ValueError, match="need max 10 rows"):
            await Pie(request, db.sql("SELECT 1,'First Name' FROM test")).build()


    @pytest.mark.asyncio
    async def test_render_pie(self, request, db):
        result = db.sql("SELECT COUNT(*),'First Name' FROM test")
        response = await Pie(request, result).build()
        assert 'plotly-graph-div' in response

    @pytest.mark.asyncio
    async def test_render_line(self, request, db):
        result = db.sql("SELECT COUNT(*),'First Name' FROM test")
        response = await Line(request, result).build()
        assert 'plotly-graph-div' in response

    
    def test_type_str(self):
        t = OptionTypeString("title", label="Title")
        assert t.render("hello \" world") == '<label for="title" class="form-label">Title</label><input value="hello &quot; world" type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
        assert t.render("") == '<label for="title" class="form-label">Title</label><input type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
        assert t.render(None) == '<label for="title" class="form-label">Title</label><input type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
        t = OptionTypeString("title", label="Title", default="Hello")
        assert t.render(None) == '<label for="title" class="form-label">Title</label><input value="Hello" type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'


    def test_type_float(self):
        t = OptionTypeFloat("title", label="Title", step=0.1)
        assert t.render(0.5) == '<label for="title" class="form-label">Title</label><input value="0.5" type="number" step="0.1" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
        t = OptionTypeFloat("title", label="Title", step=0.1, default=1)
