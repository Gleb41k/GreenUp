# tests/conftest.py
import os
import sys
from contextlib import asynccontextmanager
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import AsyncClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.core.config import settings
from app.main import app


@asynccontextmanager
async def _lifespan():
    yield


app.lifespan_context = _lifespan


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def mock_env():
    with patch.dict(
        "os.environ",
        {
            "APP_ENVIRONMENT": "test",
            "DATABASE_URL": "postgresql+asyncpg://postgres:password@localhost:5432/testdb",
            "JWT_SECRET_KEY": "test-secret",
            "CACHE_REDIS_URL": "redis://localhost:6379/1",
            "CELERY_BROKER_URL": "memory://",
            "CELERY_RESULT_BACKEND": "cache+memory://",
        },
    ):
        yield


@pytest.fixture(autouse=True)
def clean_db():
    # Создаём тестовую БД или используем in-memory
    pass


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()  # ← ОЧИСТКА ПОСЛЕ КАЖДОГО ТЕСТА
