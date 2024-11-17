import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest_asyncio
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client