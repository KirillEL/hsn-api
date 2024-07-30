from functools import wraps

from loguru import logger
from sqlalchemy import exc
from pydantic import ValidationError

from api.exceptions import (
    NotFoundException,
    ValidationException,
    InternalServerException,
)
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import session


class HandleExceptions:
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                logger.debug(f"HandleExceptions")
                return await func(*args, **kwargs)
            except NotFoundException as ne:
                raise ne
            except ValidationError as ve:
                await session.rollback()
                raise ValidationException(message=str(ve))
            except exc.SQLAlchemyError as sqle:
                await session.rollback()
                raise UnprocessableEntityException(message=str(sqle))
            except Exception as e:
                await session.rollback()
                logger.error(f"exception: {str(e)}")
                raise e

        return wrapper
