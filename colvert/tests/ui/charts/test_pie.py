
import pytest
from plotly.express.colors import qualitative

from ....ui.charts import Pie


@pytest.mark.asyncio
async def test_validate_pie_any_order(get_request, sample_db):
    result = await sample_db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL")
    pie = Pie(
        get_request,
        result,
        {},
    )
    response = await pie.build()
    # Accept the numeric argument in any order
    assert '"labels":["First Name"]' in response
    result = await sample_db.sql("SELECT 'First Name',COUNT(*) FROM test GROUP BY ALL")
    pie = Pie(
        get_request,
        result,
        {},
    )
    response = await pie.build()
    assert '"labels":["First Name"]' in response


@pytest.mark.asyncio
async def test_render_pie_options(get_request, sample_db):
    result = await sample_db.sql("SELECT COUNT(*),'First Name' FROM test")
    pie = Pie(get_request, result, {"hole": 0.5})
    assert pie.user_options == {"hole": 0.5, "color_discrete_sequence": qualitative.Vivid}
    response = await pie.build()
    assert "plotly-graph-div" in response
    assert "0.5" in response
    assert "Title" in response


@pytest.mark.asyncio
async def test_render_pie(get_request, sample_db):
    result = await sample_db.sql("SELECT COUNT(*),'First Name' FROM test")
    response = await Pie(get_request, result, {}).build()
    assert "plotly-graph-div" in response
