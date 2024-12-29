import pytest

from colvert.ai import AIError


@pytest.mark.asyncio
async def test_sql_to_prompt(http_server_sample_db, ai):
    prompt = "An amazing prompt"
    ai.return_value = "An amazing prompt"

    query = "SELECT * FROM test"
    resp = await http_server_sample_db.post("/sql-to-prompt", data={"q": query})
    assert resp.status == 200
    text = await resp.text()
    assert query in text
    assert prompt in text

@pytest.mark.asyncio
async def test_sql_to_prompt_rate_limit(http_server_sample_db, ai):
    ai.side_effect = AIError("Rate limit exceeded")

    query = "SELECT * FROM test"
    resp = await http_server_sample_db.post("/sql-to-prompt", data={"q": query})
    assert resp.status == 200
    text = await resp.text()
    assert query in text
    assert "Rate limit exceeded" in text

@pytest.mark.asyncio
async def test_prompt_to_sql(http_server_sample_db, ai):
    query = "SELECT * FROM test"
    prompt = "An amazing prompt"
    ai.return_value = f"```sql\n{query}\n```"

    resp = await http_server_sample_db.post("/prompt-to-sql", data={"prompt": prompt})
    assert resp.status == 200
    text = await resp.text()
    assert query in text
    assert prompt in text

@pytest.mark.asyncio
async def test_prompt_to_sql_rate_limit(http_server_sample_db, ai):
    prompt = "An amazing prompt"
    ai.side_effect = AIError("Rate limit exceeded")

    resp = await http_server_sample_db.post("/prompt-to-sql", data={"prompt": prompt})
    assert resp.status == 200
    text = await resp.text()
    assert prompt in text
    assert "Rate limit exceeded" in text