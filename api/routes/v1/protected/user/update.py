from typing import Optional

from pydantic import BaseModel, Field

from api.exceptions import ExceptionResponseSchema
from core.user import UserDoctorUpdateContext, user_command_update
from . import UserAndDoctorResponse
from .router import user_router
from .schemas import UserResponse
from fastapi import Request


class UpdateUserRequest(BaseModel):
    login: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=6)
    name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    cabinet_id: Optional[int] = Field(None, gt=0)


@user_router.patch(
    "",
    response_model=UserAndDoctorResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Обновить информацию о себе"
)
async def update_user(request: Request, request_body: UpdateUserRequest):
    user_id = request.user.id
    context = UserDoctorUpdateContext(
        user_id=user_id,
        **request_body.dict()
    )
    return await user_command_update(context)
