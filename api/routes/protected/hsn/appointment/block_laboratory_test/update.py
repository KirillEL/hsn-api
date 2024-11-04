from datetime import datetime
from typing import Optional

from fastapi import Request
from pydantic import BaseModel, Field, field_validator, ConfigDict

from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock, \
    HsnCommandBlockLaboratoryTestUpdateContext, hsn_command_block_laboratory_test_update
from core.hsn.appointment.blocks.laboratory_test.model import AppointmentLaboratoryTestBlockResponse
from .router import block_laboratory_test_router
from api.exceptions import ExceptionResponseSchema, ValidationException, DoctorNotAssignedException


class UpdateBlockLaboratoryTestRequestBody(BaseModel):
    nt_pro_bnp: Optional[float] = Field(None, gt=0)
    nt_pro_bnp_date: Optional[str] = Field(None)
    hbalc: Optional[float] = Field(None)
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

    protein: Optional[float] = Field(None, gt=0)
    urine_eritrocit: Optional[float] = Field(None, gt=0)
    urine_leycocit: Optional[float] = Field(None, gt=0)
    microalbumuria: Optional[float] = Field(None, gt=0)
    am_date: Optional[str] = Field(None)

    note: Optional[str] = Field(None, max_length=1000)

    @field_validator('hbalc')
    def check_hbalc_value(cls, value):
        if value is not None and value <= 0:
            raise ValidationException(message="Hbalc должно быть больше 0")

    @field_validator('nt_pro_bnp_date', 'hbalc_date', 'oak_date', 'bk_date', 'am_date')
    def check_date_format(cls, value):
        try:
            if value:
                parsed_date = datetime.strptime(value, "%d.%m.%Y")
                if parsed_date > datetime.now():
                    raise ValidationException(message="Даты не могут быть позже текущего дня")
                return value
        except ValueError:
            raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")


@block_laboratory_test_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentLaboratoryTestBlockResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def update_block_laboratory_test_route(
        request: Request,
        appointment_id: int,
        body: UpdateBlockLaboratoryTestRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandBlockLaboratoryTestUpdateContext(
        appointment_id=appointment_id,
        **body.model_dump()
    )
    doctor_id: int = request.user.doctor.id
    return await hsn_command_block_laboratory_test_update(doctor_id, context)
