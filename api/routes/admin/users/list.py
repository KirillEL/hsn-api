from .router import admin_users_router
from api.exceptions import ExceptionResponseSchema
from shared.db.models.user import UserDBModel
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from core.user import User, UserFlat


@admin_users_router.get(
    "/users",
    response_model=list[User],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_users_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(UserDBModel)
        .where(UserDBModel.is_deleted.is_(False))
    )


    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(UserDBModel.login.contains(pattern))

    cursor = await db_session.execute(query)
    users = cursor.scalars().all()
    return [User.model_validate(user) for user in users]
