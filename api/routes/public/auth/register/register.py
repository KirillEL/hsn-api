from typing import Optional
import re
from core.hsn.doctor.model import Role, UserAndDoctor

from .router import auth_register_router
from pydantic import BaseModel, Field, field_validator
from api.exceptions import ExceptionResponseSchema, ValidationException
from fastapi import Request
from core.user import user_command_create
from core.user import UserDoctorCreateContext




class UserCreateRequest(BaseModel):
    login: str = Field(..., max_length=25)
    password: str = Field(..., min_length=6)
    name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    patronymic: Optional[str] = Field(..., max_length=100)
    phone_number: str = Field(max_length=20)
    is_glav: bool = Field(False)
    role: str = Field(None)
    cabinet_id: Optional[int] = Field(None, gt=0)

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValidationException(message="Phone number is not valid")
        return v

@auth_register_router.post(
    "/",
    response_model=UserAndDoctor,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Регистрация пользователя"
)
async def register_user(req_body: UserCreateRequest):
    context = UserDoctorCreateContext(
        login=req_body.login,
        password=req_body.password,
        name=req_body.name,
        last_name=req_body.last_name,
        patronymic=req_body.patronymic,
        phone_number=req_body.phone_number,
        is_glav=req_body.is_glav,
        role=req_body.role,
        cabinet_id=req_body.cabinet_id
    )
    return await user_command_create(context)
