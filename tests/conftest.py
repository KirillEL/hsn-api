from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, SessionTransaction

from api.api_server import app
from infra import config
from shared.db.db_session import db_session
from shared.db.models import BaseDBModel


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def ac() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c


@pytest.fixture(scope="session")
def setup_db() -> Generator:
    engine = create_engine(f"{config.DB_URI.replace('+asyncpg', '+psycopg2')}")
    conn = engine.connect()
    # Terminate transaction
    conn.execute(text("commit"))
    try:
        conn.execute(text("drop database test"))
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    # Terminate transaction
    conn.execute(text("commit"))
    conn.execute(text("create database test"))
    conn.close()

    yield

    conn = engine.connect()
    # Terminate transaction
    conn.execute(text("commit"))
    try:
        conn.execute(text("drop database test"))
    except SQLAlchemyError:
        pass
    conn.close()
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(setup_db: Generator) -> Generator:
    engine = create_engine(f"test_{config.DB_URI.replace('+asyncpg', '')}")

    with engine.begin():
        BaseDBModel.metadata.drop_all(engine)
        BaseDBModel.metadata.create_all(engine)
        yield
        BaseDBModel.metadata.drop_all(engine)

    engine.dispose()


@pytest.fixture
async def session() -> AsyncGenerator:
    async_engine = create_async_engine(f"test_{config.DB_URI}")
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