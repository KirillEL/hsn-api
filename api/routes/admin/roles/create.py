from .router import admin_role_router
from sqlalchemy import insert
from shared.db.models.role import RoleDBModel
from core.user.model import Role
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema, ValidationException, InternalServerException
from pydantic import BaseModel, Field, ValidationError


class CreateRoleDto(BaseModel):
    name: str = Field(...)


@admin_role_router.post(
    "/roles",
    response_model=Role,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_role_create(dto: CreateRoleDto):
    try:
        query = (
            insert(RoleDBModel)
            .values(**dto.dict())
            .returning(RoleDBModel)
        )
        cursor = await db_session.execute(query)
        await db_session.commit()
        new_role = cursor.scalars().first()
        return Role.model_validate(new_role)
    except ValidationError as ve:
        raise ValidationException(message=str(ve))
    except Exception as e:
        await db_session.rollback()
        raise InternalServerException(message=str(e))

