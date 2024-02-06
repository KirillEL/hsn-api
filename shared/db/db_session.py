from contextvars import ContextVar, Token
from functools import wraps
from typing import Union
from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session
)
from sqlalchemy.orm import sessionmaker, Session

from infra import config

session_context: ContextVar[str] = ContextVar('session_context')


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engine = create_async_engine(config.DB_URI, echo=config.DEBUG, pool_recycle=3600)


class RouteSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        return engine.sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RouteSession,
    expire_on_commit=False
)

db_session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


class SessionContext:
    def __call__(self, func):
        @wraps(func)
        async def _session_context(*args, **kwargs):
            session_id = str(uuid4())
            context = set_session_context(session_id)

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                await db_session.remove()
                reset_session_context(context)

            return result

        return _session_context
