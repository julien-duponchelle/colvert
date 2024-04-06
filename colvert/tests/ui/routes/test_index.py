import pytest


@pytest.mark.asyncio
async def test_get_index_no_data_loaded(http_server):
    resp = await http_server.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert "CREATE TABLE" in text



@pytest.mark.asyncio
async def test_get_index_with_one_table(http_server_sample_db):
    resp = await http_server_sample_db.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert "SELECT *" in text