from enum import Enum
from functools import wraps

from loguru import logger

from shared.db.db_session import session


class Propagation(Enum):
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


async def _run_required(function, args, kwargs) -> None:
    result = await function(*args, **kwargs)
    await session.commit()
    return result


async def _run_required_new(function, args, kwargs) -> None:
    await session.begin()
    result = await function(*args, **kwargs)
    await session.commit()
    return result


class Transaction:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                if self.propagation == Propagation.REQUIRED:
                    result = await _run_required(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
                elif self.propagation == Propagation.REQUIRED_NEW:
                    result = await _run_required_new(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
                else:
                    result = await _run_required(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
            except Exception as e:
                logger.debug(f"EXCEPTION TRANSACTION ROLLBACK")
                await session.rollback()
                raise e

            return result

        return decorator
