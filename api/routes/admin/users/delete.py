from sqlalchemy import delete, update, select

from api.decorators import HandleExceptions
from .router import admin_users_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.user import UserDBModel
from api.exceptions import ExceptionResponseSchema, NotFoundException
from fastapi import Request


async def check_user_exists(user_id: int):
    query = (
        select(UserDBModel)
        .where(UserDBModel.is_deleted.is_(False))
        .where(UserDBModel.id == user_id)
    )
    cursor = await db_session.execute(query)
    user = cursor.scalars().first()
    if not user:
        raise NotFoundException("Пользователь не найден!")


@admin_users_router.delete(
    "/users/{user_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
@HandleExceptions()
async def admin_user_delete(request: Request, user_id: int):
    await check_user_exists(user_id)
    payload = {
        'is_deleted': True,
    }
    query = (
        update(UserDBModel)
        .values(**payload)
        .where(UserDBModel.id == user_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True
