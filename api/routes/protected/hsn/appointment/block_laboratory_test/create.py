from datetime import datetime

from loguru import logger

from .router import block_laboratory_test_router
from api.exceptions import ExceptionResponseSchema, ValidationException, DoctorNotAssignedException
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock, \
    hsn_command_appointment_block_laboratory_test_create, HsnCommandAppointmentBlockLaboratoryTestCreateContext
from pydantic import BaseModel, Field, field_validator
from datetime import date as tdate
from typing import Optional
from fastapi import Request


class CreateBlockLaboratoryTestRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    nt_pro_bnp: float = Field(gt=0)
    nt_pro_bnp_date: str = Field(default=datetime.today().strftime("%d.%m.%Y"))
    hbalc: float = Field(gt=0)
    hbalc_date: str = Field(default=datetime.today().strftime("%d.%m.%Y"))

    eritrocit: float = Field(gt=0)
    hemoglobin: float = Field(gt=0)
    oak_date: str = Field(default=datetime.today().strftime("%d.%m.%Y"))

    tg: float = Field(gt=0)
    lpvp: float = Field(gt=0)
    lpnp: float = Field(gt=0)
    general_hc: float = Field(gt=0)
    natriy: float = Field(gt=0)
    kaliy: float = Field(gt=0)
    glukoza: float = Field(gt=0)
    mochevaya_kislota: float = Field(gt=0)
    skf: float = Field(gt=0)
    kreatinin: float = Field(gt=0)
    bk_date: str = Field(default=datetime.today().strftime("%d.%m.%Y"))

    protein: float = Field(gt=0)
    urine_eritrocit: float = Field(gt=0)
    urine_leycocit: float = Field(gt=0)
    microalbumuria: float = Field(gt=0)
    am_date: str = Field(default=datetime.today().strftime("%d.%m.%Y"))
    note: Optional[str] = Field(None, max_length=1000)

    @field_validator('nt_pro_bnp_date', 'hbalc_date', 'bk_date', 'oak_date', 'am_date')
    def check_date_format(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            if parsed_date > datetime.now():
                raise ValidationException(message="Даты не могут быть позднее текущего дня")
            return value
        except ValueError:
            raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")


@block_laboratory_test_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_laboratory_test_route(
        request: Request,
        body: CreateBlockLaboratoryTestRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentBlockLaboratoryTestCreateContext(**body.model_dump())
    return await hsn_command_appointment_block_laboratory_test_create(context)
