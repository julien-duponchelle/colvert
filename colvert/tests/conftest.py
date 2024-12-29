from unittest.mock import AsyncMock

import pytest
import pytest_asyncio


@pytest.fixture()
def ai(monkeypatch):
    import colvert.ai

    monkeypatch.delattr("litellm.acompletion") # Prevent outside calls
    mock_response = AsyncMock()
    monkeypatch.setattr(colvert.ai, "_completion", mock_response)
    return mock_response


@pytest_asyncio.fixture(scope="session")
async def sample_db():
    from colvert.database import Database
    
    db = Database()
    await db.load_files(["./samples/test.csv"])
    return db