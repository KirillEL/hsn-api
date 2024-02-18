from pydantic import BaseModel

from core.user.queries.me import hsn_user_get_me
from .router import user_router
from api.exceptions import ExceptionResponseSchema, NotFoundException
from fastapi import Request
from typing import Optional


class DoctorResponse(BaseModel):
    id: int
    name: str
    last_name: str
    patronymic: str
    is_glav: bool
    cabinet_id: Optional[int] = None


class UserAndDoctorResponse(BaseModel):
    id: int
    login: str
    role: str
    doctor: DoctorResponse


@user_router.get(
    "/me",
    response_model=UserAndDoctorResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_current_user(request: Request):
    return await hsn_user_get_me(request.user.id)

