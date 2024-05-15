from functools import wraps

from loguru import logger
from sqlalchemy import exc
from pydantic import ValidationError

from api.exceptions import NotFoundException, ValidationException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session


class HandleExceptions:
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except NotFoundException as ne:
                raise ne
            except ValidationError as ve:
                await db_session.rollback()
                raise ValidationException(message=str(ve))
            except exc.SQLAlchemyError as sqle:
                await db_session.rollback()
                raise UnprocessableEntityException(message=str(sqle))
            except Exception as e:
                await db_session.rollback()
                logger.error(f'exception: {str(e)}')
                raise InternalServerException

        return wrapper
