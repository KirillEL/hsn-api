from contextvars import ContextVar, Token
from functools import wraps
from typing import Union
from uuid import uuid4

from loguru import logger
from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session
)
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from infra import config

session_context: ContextVar[str] = ContextVar('session_context')


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engine = create_async_engine(config.DB_URI, echo=config.DEBUG, pool_recycle=3600)

async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    future=True,
)
session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context
)