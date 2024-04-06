import json

import pytest


@pytest.mark.asyncio
async def test_completion(http_server_sample_db):
    resp = await http_server_sample_db.post(
        "/completion",
        data=json.dumps({"q": "SELECT * FROM te"})
    )
    assert resp.status == 200
    suggestions = await resp.json()
    assert {'kind' : 'Class', 'label' : 'test', 'text': 'test'} in suggestions