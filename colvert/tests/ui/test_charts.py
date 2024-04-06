import pytest

from ...database import Database
from ...ui.charts import Pie


class TestCharts:
    @pytest.fixture(scope="class")
    def db(self):
        db = Database()
        db.load_file("./samples/test.csv")
        return db
    
    def test_validate_pie(self, db):
        Pie(db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL")).build()
        with pytest.raises(ValueError, match="2 columns"):
            Pie(db.sql("SELECT COUNT(*) FROM test")).build()
        with pytest.raises(ValueError, match="NUMBER"):
            Pie(db.sql("SELECT 'First Name','Last Name' FROM test")).build()
        with pytest.raises(ValueError, match="need max 10 rows"):
            Pie(db.sql("SELECT 1,'First Name' FROM test")).build()


    def test_render_pie(self, db):
        result = db.sql("SELECT COUNT(*),'First Name' FROM test")
        response = Pie(result).build()
        assert response.status == 200
        assert response.text
        assert 'plotly-graph-div' in response.text