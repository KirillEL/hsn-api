from sqlalchemy import select
from shared.db.models.role import RoleDBModel
from .router import admin_role_router
from shared.db.db_session import db_session, SessionContext
from core.user.model import Role
from api.exceptions import ExceptionResponseSchema


@admin_role_router.get(
    "/roles",
    response_model=list[Role],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_roles_list():
    query = select(RoleDBModel)
    cursor = await db_session.execute(query)
    roles = cursor.scalars().all()

    return [Role.model_validate(r) for r in roles]
