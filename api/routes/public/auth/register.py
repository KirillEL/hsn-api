from .router import auth_router
from pydantic import BaseModel, Field
from api.exceptions import ExceptionResponseSchema
from fastapi import Request
from core.user import user_command_create
from fastapi.exceptions import HTTPException
from core.user import UserCreateContext
from shared.db.commands import db_base_entity_create


class UserCreateResponse(BaseModel):
    id: int
    login: str


class UserCreateRequest(BaseModel):
    login: str = Field(..., max_length=25)
    password: str = Field(..., min_length=6)


@auth_router.post(
    "/register",
    response_model=UserCreateResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def register_user(request: Request, params: UserCreateRequest):
    context = UserCreateContext(login=params.login, password=params.password)
    return await user_command_create(context)
