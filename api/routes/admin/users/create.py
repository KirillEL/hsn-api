from shared.db.models.user import UserDBModel
from utils import PasswordHasher
from .router import admin_users_router
from shared.db.db_session import SessionContext, db_session
from core.user import User
from api.exceptions import ExceptionResponseSchema
from fastapi import Request
from pydantic import BaseModel, Field
from sqlalchemy import insert


class CreateUserDto(BaseModel):
    login: str = Field(...)
    password: str = Field(min_length=6)


@admin_users_router.post(
    "/users",
    response_model=User,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_user_create(dto: CreateUserDto):
    query = (
        insert(UserDBModel)
        .values(
            login=dto.login,
            password=PasswordHasher.hash_password(dto.password)
        )
        .returning(UserDBModel)
    )
    cursor = await db_session.execute(query)
    new_user = cursor.scalars().first()
    return User.model_validate(new_user)
