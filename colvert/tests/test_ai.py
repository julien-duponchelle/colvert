import os
from unittest import mock

import pytest

import colvert.ai


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "AAAA"}):
        yield


@pytest.mark.asyncio
async def test_prompt_to_sql(sample_db, ai):        
    ai.return_value = "```sql\nSELECT * FROM table```"
    result = await colvert.ai.prompt_to_sql(sample_db, "Hello")
    assert result == "SELECT * FROM table"

@pytest.mark.asyncio
async def test_sql_to_prompt(ai):
    ai.return_value = "Hello"
    result = await colvert.ai.sql_to_prompt("SELECT * FROM table")
    assert result == "Hello"
