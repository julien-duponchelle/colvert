
import pytest


@pytest.mark.asyncio
async def test_index(http_server):
    resp = await http_server.get("/docs")
    assert resp.status == 200
    content = await resp.content.read()
    assert b'Charts' in content

@pytest.mark.asyncio
async def test_path(http_server):
    resp = await http_server.get("/docs/charts/pie/index")
    assert resp.status == 200
    content = await resp.content.read()
    assert b'Hole' in content

@pytest.mark.asyncio
async def test_admonition(http_server):
    resp = await http_server.get("/docs/getting-started")
    assert resp.status == 200
    content = await resp.content.read()
    assert b'alert alert-warning' in content

@pytest.mark.asyncio
async def test_path_index(http_server):
    resp = await http_server.get("/docs/charts/pie/")
    assert resp.status == 200
    content = await resp.content.read()
    assert b'Hole' in content

@pytest.mark.asyncio
async def test_png(http_server):
    resp = await http_server.get("/docs/charts/pie/pie.png")
    assert resp.status == 200
    content = await resp.content.read()
    assert b'PNG' in content

@pytest.mark.asyncio
async def test_404(http_server):
    resp = await http_server.get("/docs/404")
    assert resp.status == 404