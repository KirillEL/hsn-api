from typing import Optional

from sqlalchemy import select, insert
from .router import admin_doctor_router
from shared.db.models.doctor import DoctorDBModel
from core.hsn.doctor import Doctor
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from fastapi import Request

class CreateDoctorDto(BaseModel):
    name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    phone_number: int = Field(gt=0)
    user_id: int = Field(gt=0)
    cabinet_id: int = Field(gt=0)
    is_glav: bool = Field(False)



@admin_doctor_router.post(
    "/doctors",
    response_model=Doctor,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_doctor_create(request: Request, dto: CreateDoctorDto):
    query = (
        insert(DoctorDBModel)
        .values(
            **dto.dict(),
            author_id=request.user.id
        )
        .returning(DoctorDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_doctor = cursor.unique().scalars().first()

    return Doctor.model_validate(new_doctor)