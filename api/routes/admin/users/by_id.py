from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .router import admin_users_router
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema, NotFoundException
from core.user import User, UserFlat
from shared.db.models.user import UserDBModel


@admin_users_router.get(
    "/users/{user_id}",
    response_model=UserFlat,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_user_by_id(user_id: int):
    query = (
        select(UserDBModel)
        .options(joinedload(UserDBModel.roles))
        .where(UserDBModel.id == user_id)
    )
    cursor = await db_session.execute(query)
    user = cursor.scalars().first()
    if user is None:
        raise NotFoundException(message="пользователь не найден!")
    return UserFlat.model_validate(user)
