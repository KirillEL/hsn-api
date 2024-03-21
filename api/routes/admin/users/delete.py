from sqlalchemy import delete, update
from .router import admin_users_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.user import UserDBModel
from api.exceptions import ExceptionResponseSchema
from fastapi import Request

@admin_users_router.delete(
    "/users/{user_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_user_delete(request: Request, user_id: int):
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