import asyncio
from typing import AsyncGenerator
import os
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from select import select
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

from api.api_server import app as application
from api.routes.admin.roles import admin_role_by_id
from core.on_startup import hsn_create_admin
from infra import config
from shared.db.db_session import db_session
from shared.db.models import UserDBModel
from shared.db.models.role import RoleDBModel
from shared.db.models.user_role import UserRoleDBModel
from utils import PasswordHasher

load_dotenv()

DB_SERVER = os.environ.get("DB_SERVER")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

TEST_USERNAME = os.environ.get("TEST_USER")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

test_async_session_factory = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_async_session():
    async with test_async_session_factory() as async_session:
        yield async_session


application.dependency_overrides[db_session] = override_get_async_session


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client():
    with TestClient(application) as c:
        yield c


@pytest.fixture(scope="session")
def test_user():
    return {
        "login": TEST_USERNAME,
        "password": TEST_PASSWORD
    }


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=application, base_url="http://localhost:9999/api/v1",
                           headers={"Content-Type": "application/json"}) as ac:
        yield ac


@pytest.fixture(autouse=True)
async def transaction():
    async with test_async_session_factory.begin() as session:
        yield session
        await session.rollback()
