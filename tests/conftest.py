import asyncio
import subprocess
from typing import AsyncGenerator
import os
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from loguru import logger
from sqlalchemy import text, insert, select, MetaData, inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

from api.api_server import app as application
from infra import config
from shared.db.db_session import db_session
from shared.db.models import UserDBModel, MedOrganizationDBModel, CabinetDBModel
from shared.db.models.role import RoleDBModel
from shared.db.models.user_role import UserRoleDBModel
from utils import PasswordHasher

load_dotenv()

# Environment variables for the test database
TEST_DB_SERVER = "test_database"
TEST_DB_PORT = "5432"
TEST_DB_NAME = "test_db"
TEST_DB_USER = "testuser"
TEST_DB_PASSWORD = "testuserpassword"

TEST_USERNAME = "testuser1"
TEST_PASSWORD = "testuserpassword1"

DATABASE_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_SERVER}:{TEST_DB_PORT}/{TEST_DB_NAME}"

faker = Faker()

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


async def set_up_roles():
    async with test_async_session_factory.begin() as session:
        role = RoleDBModel(name="admin")
        role_2 = RoleDBModel(name="doctor")
        session.add(role)
        session.add(role_2)


async def set_up_med_org():
    async with test_async_session_factory.begin() as session:
        med_org = MedOrganizationDBModel(
            name=faker.company(),
            number=faker.random_int(5, 500),
            address=faker.address(),
            author_id=1
        )
        session.add(med_org)
        return med_org.id


async def set_up_cabinet():
    med_id = await set_up_med_org()
    async with test_async_session_factory.begin() as session:
        cabinet = CabinetDBModel(
            number=faker.text(max_nb_chars=255),
            med_id=med_id,
            author_id=1
        )
        session.add(cabinet)
        await session.flush()
        return cabinet.id



async def set_up_admin():
    async with test_async_session_factory.begin() as session:
        await create_admin_for_tests(session=session)


async def create_admin_for_tests(session):
    new_user = UserDBModel(login='admin%&', password=PasswordHasher.hash_password(config.ADMIN_PASS))
    session.add(new_user)
    await session.flush()

    query_select_role_admin = (
        select(RoleDBModel)
        .where(RoleDBModel.name == "admin")
    )
    cursor = await session.execute(query_select_role_admin)
    admin_role_id = cursor.scalar_one().id

    query_add_user_role = (
        insert(UserRoleDBModel)
        .values(
            user_id=new_user.id,
            role_id=admin_role_id
        )
        .returning(UserRoleDBModel.user_id)
    )
    await session.execute(query_add_user_role)
    await session.commit()


async def run_shell_script(script_name: str):
    process = await asyncio.create_subprocess_shell(
        f"/bin/sh {script_name}",
        env={"DATABASE_URL": DATABASE_URL},
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f"Error running {script_name}: {stderr.decode()}")
    else:
        print(f"{script_name} output: {stdout.decode()}")


@pytest.fixture(scope="session", autouse=True)
async def prepare_test_database():
    await run_shell_script("upgrade_test_db.sh")
    #await set_up_roles()
    #await set_up_admin()
    #await set_up_cabinet()
    yield
    #await run_shell_script("downgrade_test_db.sh")


@pytest.fixture(scope="session")
def event_loop(request):
    logger.debug(f'event_loop: {event_loop}')
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_user():
    return {
        "login": TEST_USERNAME,
        "password": TEST_PASSWORD
    }


@pytest.fixture(scope="session")
async def cabinet_id():
    return await set_up_cabinet()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=application), base_url="http://localhost:9999/api/v1") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def transaction():
    async with test_async_session_factory.begin() as session:
        yield session
