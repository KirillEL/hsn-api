from sqlalchemy import delete
from shared.db.models.role import RoleDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_role_router
from api.exceptions import ExceptionResponseSchema


@admin_role_router.delete(
    "/roles/{role_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_role_delete(role_id: int):
    query = (
        delete(RoleDBModel)
        .where(RoleDBModel.id == role_id)
    )
    await db_session.execute(query)
    return True
