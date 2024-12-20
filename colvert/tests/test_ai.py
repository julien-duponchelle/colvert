import os
from unittest import mock
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from colvert.ai import AI
from colvert.database import Database


class TestAI:
    @pytest.fixture(autouse=True)
    def mock_settings_env_vars(self):
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "AAAA"}):
            yield

    @pytest_asyncio.fixture(scope="class")
    async def db(self):
        db = Database()
        await db.load_files(["./samples/test.csv"])
        return db
    
    @pytest.fixture()
    def ai(self, monkeypatch):
        ai = AI()
        mock_response = AsyncMock()
        monkeypatch.setattr(ai, "_completion", mock_response)
        return ai

    @pytest.mark.asyncio
    async def test_prompt_to_sql(self, db, ai):        
        ai._completion.return_value = "```sql\nSELECT * FROM table```"
        result = await ai.prompt_to_sql(db, "Hello")
        assert result == "SELECT * FROM table"
    
    @pytest.mark.asyncio
    async def test_sql_to_prompt(self, db, ai):
        ai._completion.return_value = "Hello"
        result = await ai.sql_to_prompt("SELECT * FROM table")
        assert result == "Hello"
