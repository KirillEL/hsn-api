from shared.db.models.role import RoleDBModel
from shared.db.models.user import UserDBModel
from shared.db.models.user_role import UserRoleDBModel
from utils import PasswordHasher
from .router import admin_users_router
from shared.db.db_session import SessionContext, db_session
from core.user import User, UserFlat
from api.exceptions import ExceptionResponseSchema
from fastapi import Request
from pydantic import BaseModel, Field
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload
from api.exceptions import NotFoundException


class CreateUserDto(BaseModel):
    login: str = Field(...)
    password: str = Field(min_length=6)
    role: str = Field(None)


async def check_role_exists(role: str) -> None | int:
    query = (
        select(RoleDBModel)
        .where(RoleDBModel.name == role)
    )
    cursor = await db_session.execute(query)
    role = cursor.scalars().first()
    if role is None:
        raise NotFoundException(message="Роль не найдена")

    return role.id


@admin_users_router.post(
    "/users",
    response_model=UserFlat,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_user_create(dto: CreateUserDto):
    try:
        role_id = await check_role_exists(dto.role)
        query = (
            insert(UserDBModel)
            .values(
                login=dto.login,
                password=PasswordHasher.hash_password(dto.password)
            )
            .returning(UserDBModel.id)
        )
        cursor = await db_session.execute(query)
        new_user_id = cursor.scalar()

        query_add_user_role = (
            insert(UserRoleDBModel)
            .values(
                user_id=new_user_id,
                role_id=role_id
            )
            .returning(None)
        )
        await db_session.execute(query_add_user_role)

        query_get_new_user = (
            select(UserDBModel)
            .options(joinedload(UserDBModel.roles))
            .where(UserDBModel.id ==new_user_id)
        )
        cursor = await db_session.execute(query_get_new_user)
        await db_session.commit()
        new_user = cursor.scalars().first()

        return UserFlat.model_validate(new_user)
    except Exception as e:
        await db_session.rollback()
        raise e