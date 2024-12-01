import pytest
import pytest_asyncio
from pandas import DataFrame
from plotly.express.colors import qualitative

from ....ui.charts import Line


@pytest_asyncio.fixture(scope="session")
async def result(sample_db):
    return await sample_db.sql("SELECT 'First Name',COUNT(*) FROM test")


@pytest.mark.asyncio
async def test_render_line(get_request, result):
    response = await Line(get_request, result, {}).build()
    assert "plotly-graph-div" in response
    # Test default
    assert 'Vivid" selected' in response


@pytest.mark.asyncio
async def test_line_user_options(get_request, result):
    line = Line(get_request, result, {"facet": None})
    assert line.user_options == {"color_discrete_sequence": qualitative.Vivid}
    line = Line(get_request, result, {"facet": ""})
    assert line.user_options == {"color_discrete_sequence": qualitative.Vivid}
    line = Line(get_request, result, {"facet": "First Name"})
    assert line.user_options == {
        "facet": "First Name",
        "color_discrete_sequence": qualitative.Vivid,
    }


@pytest.mark.asyncio
async def test_get_x_y_column_names(get_request, sample_db):
    result = await sample_db.sql("SELECT 'First Name' as name,Salary FROM test")
    line = Line(get_request, result, {})
    assert line._get_x_y_column_names(result) == ("name", ["Salary"])
    result = await sample_db.sql("SELECT 'First Name' as name,Salary,Bonus FROM test")
    line = Line(get_request, result, {})
    assert line._get_x_y_column_names(result) == ("name", ["Salary", "Bonus"])
    result = await sample_db.sql("SELECT 'First Name' as name,Salary,Bonus,Gender FROM test")
    line = Line(get_request, result, {"facet": "Gender"})
    assert line._get_x_y_column_names(result, ) == ("name", ["Salary", "Bonus"])


@pytest.mark.asyncio
async def test_traces(sample_db, get_request):
    result = await sample_db.sql("SELECT 'First Name' as name,Salary FROM test")
    line = Line(get_request, result, {})
    data = {
        'Year': ['1990', '1991', '1992', '1993'],
        'Sales': [20, 21, 19, 18],
        'Expenses': [10, 11, 12, 13],
    }
    df = DataFrame(data)
    result = list(line._traces(df, ['Sales']))
    assert len(result) == 1
    assert result[0][0] == 'Sales'
    assert len(result[0][1]['Year']) == 4
    assert len(result[0][1]['Sales']) == 4


@pytest.mark.asyncio
async def test_traces_facet(sample_db, get_request):
    result = await sample_db.sql("SELECT 'First Name' as name,Salary FROM test")
    line = Line(get_request, result, {'facet': 'City'})
    data = {
        'Year': [
            '1990', '1991', '1992', '1993',
            '1990','1991', '1992', '1993'
        ],
        'Sales': [
            20, 21, 19, 18,
            30, 31, 32, 33
        ],
        'Expenses': [
            10, 11, 12, 13,
            22, 23, 24, 25    
        ],
        'City': [
            'New York', 'New York', 'New York', 'New York',
            'Paris', 'Paris', 'Paris', 'Paris'         
        ],
    }
    df = DataFrame(data)
    result = list(line._traces(df, ['Sales']))
    assert len(result) == 2
    assert result[0][0] == 'Sales'
    assert len(result[0][1]['Year']) == 4
    assert len(result[0][1]['Sales']) == 4
    assert len(result[1][1]['Year']) == 4
    assert len(result[1][1]['Sales']) == 4
    assert result[0][1]['Sales'].iat[0] == 20
    assert result[1][1]['Sales'].iat[0] == 30
    assert result[0][1]['City'].iat[0] == 'New York'
    assert result[1][1]['City'].iat[0] == 'Paris'