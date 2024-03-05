from shared.db.db_session import db_session, SessionContext
from shared.db.models.role import RoleDBModel
from sqlalchemy import select
from core.user.model import Role
from .router import admin_role_router
from api.exceptions import ExceptionResponseSchema, NotFoundException


@admin_role_router.get(
    "/admin/roles/{role_id}",
    response_model=Role,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_role_by_id(role_id: int):
    query = (
        select(RoleDBModel)
        .where(RoleDBModel.id == role_id)
    )
    cursor = await db_session.execute(query)
    role = cursor.scalars().first()
    if role is None:
        raise NotFoundException(message="Роль не найдена!")

    return role