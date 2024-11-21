import asyncio
from typing import AsyncGenerator, Generator
from dotenv import load_dotenv
import pytest
from httpx import AsyncClient
import os

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.api_server import app
from shared.db.db_session import db_session

load_dotenv()

DB_SERVER = os.environ.get("DB_SERVER")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

TEST_USER = os.environ.get("TEST_USER")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD")

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
)

test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool, echo=False)

test_async_session_factory = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_async_session():
    async with test_async_session_factory() as async_session:
        yield async_session


app.dependency_overrides[db_session] = override_get_async_session


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_user():
    return {"login": TEST_USER, "password": TEST_PASSWORD}


async def test_login(ac: AsyncClient, test_user):
    response = await ac.post("/auth/login", json=test_user)
    assert response.status_code == 200
    token = response.json()["token"]
    assert token is not None
    return token


@pytest.fixture
async def test_token(ac: AsyncClient, test_user):
    token = await test_login(ac, test_user)
    yield token


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost:9999/api/v1") as ac:
        yield ac


@pytest.fixture(scope="function", autouse=True)
async def transaction():
    async with test_async_session_factory.begin() as session:
        yield session
        await session.rollback()
