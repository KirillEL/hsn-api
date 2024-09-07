from sqlalchemy.orm import joinedload

from api.decorators import HandleExceptions
from core.user.model import UserWithPasswordFlat
from .router import admin_users_router
from api.exceptions import ExceptionResponseSchema
from shared.db.models.user import UserDBModel
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from core.user import User, UserFlat


@admin_users_router.get(
    "/users",
    response_model=list[UserWithPasswordFlat],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
@HandleExceptions()
async def admin_users_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(UserDBModel)
        .options(joinedload(UserDBModel.roles))
        .where(UserDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(UserDBModel.login.contains(pattern))

    cursor = await db_session.execute(query)
    users = cursor.unique().scalars().all()

    return [UserWithPasswordFlat.model_validate(user) for user in users]