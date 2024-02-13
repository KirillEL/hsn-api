from pydantic import BaseModel

from core.user.queries.me import hsn_user_get_me
from .router import user_router
from api.exceptions import ExceptionResponseSchema, NotFoundException
from fastapi import Request
from core.hsn.doctor import Doctor
from .schemas import UserResponse
from core.hsn.doctor.model import UserAndDoctor


class DoctorResponse(BaseModel):
    id: int
    name: str
    last_name: str
    patronymic: str
    is_glav: bool


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
async def get_current_user(req: Request):
    doctor = await hsn_user_get_me(req.user.id)
    return doctor
