from sqlalchemy import select
from .router import admin_users_router
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema
from core.user import User
from shared.db.models.user import UserDBModel


@admin_users_router.get(
    "/users/{user_id}",
    response_model=User,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_user_by_id(user_id: int):
    query = (
        select(UserDBModel)
        .where(UserDBModel.id == user_id)
    )
    cursor = await db_session.execute(query)
    user = cursor.scalars().first()

    return User.model_validate(user)
