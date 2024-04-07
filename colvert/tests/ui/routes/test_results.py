
import pytest


@pytest.mark.asyncio
async def test_post_results(http_server_sample_db):
    resp = await http_server_sample_db.post(
        "/results",
        data={
            "q": "SELECT COUNT(*) as test_count FROM test"
        }
    )
    assert resp.status == 200
    assert "test_count" in await resp.text()


@pytest.mark.asyncio
async def test_post_results_pie(http_server_sample_db):
    resp = await http_server_sample_db.post(
        "/results",
        data={
            "q": 'SELECT COUNT(*),"First Name" FROM test GROUP BY ALL',
            "chart": "pie",
            "side-by-side": False
        }
    )
    assert resp.status == 200
    assert "plotly-graph-div" in await resp.text()


@pytest.mark.asyncio
async def test_post_results_pie_side_by_side(http_server_sample_db):
    resp = await http_server_sample_db.post(
        "/results",
        data={
            "q": 'SELECT COUNT(*),"First Name" FROM test GROUP BY ALL',
            "chart": "pie",
            "side-by-side": True
        }
    )
    assert resp.status == 200
    assert "plotly-graph-div" in await resp.text()

@pytest.mark.asyncio
async def test_post_results_error(http_server_sample_db):
    resp = await http_server_sample_db.post(
        "/results",
        data={
            "q": 'SELECT COUNT(*),"First',
            "chart": "pie"
        }
    )
    assert resp.status == 200
    assert "Parser Error:" in await resp.text()
    