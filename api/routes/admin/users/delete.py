from sqlalchemy import delete
from .router import admin_users_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.user import UserDBModel
from api.exceptions import ExceptionResponseSchema


@admin_users_router.delete(
    "/users/{user_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_user_delete(user_id: int):
    query = (
        delete(UserDBModel)
        .where(UserDBModel.id == user_id)
    )
    await db_session.execute(query)
    return True