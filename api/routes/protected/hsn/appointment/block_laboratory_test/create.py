from datetime import datetime

from loguru import logger

from .router import block_laboratory_test_router
from api.exceptions import (
    ExceptionResponseSchema,
    ValidationException,
    DoctorNotAssignedException,
)
from core.hsn.appointment.blocks.laboratory_test import (
    AppointmentLaboratoryTestBlock,
    hsn_command_appointment_block_laboratory_test_create,
    HsnCommandAppointmentBlockLaboratoryTestCreateContext,
)
from pydantic import BaseModel, Field, field_validator
from datetime import date as tdate
from typing import Optional
from fastapi import Request


class CreateBlockLaboratoryTestRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    nt_pro_bnp: Optional[float] = Field(None, gt=0)
    nt_pro_bnp_date: Optional[str] = Field(None)
    hbalc: Optional[float] = Field(None, gt=0)
    hbalc_date: Optional[str] = Field(None)

    eritrocit: Optional[float] = Field(None, gt=0)
    hemoglobin: Optional[float] = Field(None, gt=0)
    oak_date: Optional[str] = Field(None)

    tg: Optional[float] = Field(None, gt=0)
    lpvp: Optional[float] = Field(None, gt=0)
    lpnp: Optional[float] = Field(None, gt=0)
    general_hc: Optional[float] = Field(None, gt=0)
    natriy: Optional[float] = Field(None, gt=0)
    kaliy: Optional[float] = Field(None, gt=0)
    glukoza: Optional[float] = Field(None, gt=0)
    mochevaya_kislota: Optional[float] = Field(None, gt=0)
    skf: Optional[float] = Field(None, gt=0)
    kreatinin: Optional[float] = Field(None, gt=0)
    bk_date: Optional[str] = Field(None)

    protein: Optional[str] = Field(None)
    urine_eritrocit: Optional[str] = Field(None)
    urine_leycocit: Optional[str] = Field(None)
    microalbumuria: Optional[str] = Field(None)
    am_date: Optional[str] = Field(None)
    note: Optional[str] = Field(None, max_length=1000)

    @field_validator("nt_pro_bnp_date", "hbalc_date", "bk_date", "oak_date", "am_date")
    def check_date_format(cls, value):
        try:
            if value:
                parsed_date = datetime.strptime(value, "%d.%m.%Y")
                if parsed_date > datetime.now():
                    raise ValidationException(
                        message="Даты не могут быть позднее текущего дня"
                    )
                return value
        except ValueError:
            raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")


@block_laboratory_test_router.post(
    "/create", response_model=int, responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_laboratory_test_route(
    request: Request, body: CreateBlockLaboratoryTestRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentBlockLaboratoryTestCreateContext(**body.model_dump())
    doctor_id: int = request.user.doctor.id
    return await hsn_command_appointment_block_laboratory_test_create(
        doctor_id, context
    )
