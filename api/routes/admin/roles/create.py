from .router import admin_role_router
from sqlalchemy import insert
from shared.db.models.role import RoleDBModel
from core.user.model import Role
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field


class CreateRoleDto(BaseModel):
    name: str = Field(...)


@admin_role_router.post(
    "/roles",
    response_model=Role,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_role_create(dto: CreateRoleDto):
    query = (
        insert(RoleDBModel)
        .values(**dto)
        .returning(RoleDBModel)
    )
    cursor = await db_session.execute(query)
    new_role = cursor.scalars().first()
    return Role.model_validate(new_role)
