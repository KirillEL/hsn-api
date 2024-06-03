from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine, event, text, select, func, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import Session, SessionTransaction, sessionmaker

from api.api_server import app
from infra import config
from shared.db.db_session import db_session
from shared.db.models import BaseDBModel, MedOrganizationDBModel, CabinetDBModel, UserDBModel
from shared.db.models.role import RoleDBModel
from shared.db.models.user_role import UserRoleDBModel
from utils import PasswordHasher


async def create_admin(session: AsyncSession):
    query_check_admin_role = (
        select(func.count())
        .select_from(RoleDBModel)
        .where(RoleDBModel.name == 'admin')
    )
    result = await session.execute(query_check_admin_role)
    admin_count = result.scalar()
    if admin_count == 0:
        role = RoleDBModel(name='admin')
        session.add(role)
        await session.commit()

        admin_role_id = role.id
    else:
        role = await session.execute(select(RoleDBModel).where(RoleDBModel.name == 'admin'))
        admin_role_id = role.scalar_one().id

    query_check_admin_user = (
        select(func.count())
        .select_from(UserDBModel)
        .join(UserRoleDBModel)
        .where(UserRoleDBModel.role_id == admin_role_id)
    )
    res = await session.execute(query_check_admin_user)
    admin_user_count = res.scalar()

    if admin_user_count == 0:
        new_user = UserDBModel(login='admin%&', password=PasswordHasher.hash_password(config.ADMIN_PASS))
        session.add(new_user)
        await session.flush()

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


async def create_med_org(session: AsyncSession):
    med_org = MedOrganizationDBModel(
        name="med_org_1",
        number=101,
        address="123 Main St",
        author_id=1
    )
    session.add(med_org)
    await session.commit()


async def create_cabinet(session: AsyncSession):
    cabinet = CabinetDBModel(
        number="cabinet_1",
        med_id=1,
        author_id=1
    )
    session.add(cabinet)
    await session.commit()


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def ac() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost:9999/api/v1") as c:
        yield c


@pytest.fixture(scope="session")
def setup_db() -> Generator:
    engine = create_engine(f"{config.DB_TEST_URI.replace('+asyncpg', '+psycopg2')}")
    conn = engine.connect()
    conn.execute(text("commit"))
    try:
        conn.execute(text("drop database test_hsn_db;"))
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    conn.execute(text("commit"))
    conn.execute(text("create database test_hsn_db;"))
    conn.close()

    yield

    conn = engine.connect()
    # Terminate transaction
    conn.execute(text("commit"))
    try:
        pass
        conn.execute(text("drop database test_hsn_db;"))
    except SQLAlchemyError:
        pass
    conn.close()
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(setup_db: Generator) -> Generator:
    engine = create_engine(f"{config.DB_TEST_URI.replace('+asyncpg', '')}")
    SessionLocal = sessionmaker(bind=engine, future=True)
    with engine.begin():
        BaseDBModel.metadata.drop_all(engine)
        BaseDBModel.metadata.create_all(engine)
        yield
        BaseDBModel.metadata.drop_all(engine)

    engine.dispose()


@pytest.fixture
async def session() -> AsyncGenerator:
    async_engine = create_async_engine(f"{config.DB_TEST_URI}")
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session: Session, transaction: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[db_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()

    await async_engine.dispose()


@pytest.fixture
async def create_start_data(session: AsyncSession):
    session = session
    session.add(RoleDBModel(name="admin"))
    session.add(RoleDBModel(name="doctor"))
    await session.commit()
    await create_admin(session)
    await create_med_org(session)
    await create_cabinet(session)
