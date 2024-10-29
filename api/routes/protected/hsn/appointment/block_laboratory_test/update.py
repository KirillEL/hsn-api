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
    eritrocit_date: Optional[str] = Field(None)
    hemoglobin: Optional[float] = Field(None, gt=0)
    hemoglobin_date: Optional[str] = Field(None)
    tg: Optional[float] = Field(None, gt=0)
    tg_date: Optional[str] = Field(None)
    lpvp: Optional[float] = Field(None, gt=0)
    lpvp_date: Optional[str] = Field(None)
    lpnp: Optional[float] = Field(None, gt=0)
    lpnp_date: Optional[str] = Field(None)
    general_hc: Optional[float] = Field(None, gt=0)
    general_hc_date: Optional[str] = Field(None)
    natriy: Optional[float] = Field(None, gt=0)
    natriy_date: Optional[str] = Field(None)
    kaliy: Optional[float] = Field(None, gt=0)
    kaliy_date: Optional[str] = Field(None)
    glukoza: Optional[float] = Field(None, gt=0)
    glukoza_date: Optional[str] = Field(None)
    mochevaya_kislota: Optional[float] = Field(None, gt=0)
    mochevaya_kislota_date: Optional[str] = Field(None)
    skf: Optional[float] = Field(None, gt=0)
    skf_date: Optional[str] = Field(None)
    kreatinin: Optional[float] = Field(None, gt=0)
    kreatinin_date: Optional[str] = Field(None)
    protein: Optional[float] = Field(None, gt=0)
    protein_date: Optional[str] = Field(None)
    urine_eritrocit: Optional[float] = Field(None, gt=0)
    urine_eritrocit_date: Optional[str] = Field(None)
    urine_leycocit: Optional[float] = Field(None, gt=0)
    urine_leycocit_date: Optional[str] = Field(None)
    microalbumuria: Optional[float] = Field(None, gt=0)
    microalbumuria_date: Optional[str] = Field(None)
    note: Optional[str] = Field(None, max_length=1000)

    @field_validator('hbalc')
    def check_hbalc_value(cls, value):
        if value is not None and value <= 0:
            raise ValidationException(message="Hbalc должно быть больше 0")

    @field_validator('nt_pro_bnp_date', 'hbalc_date', 'eritrocit_date',
                     'hemoglobin_date', 'tg_date', 'lpvp_date', 'lpnp_date',
                     'general_hc_date', 'natriy_date', 'kaliy_date', 'glukoza_date',
                     'mochevaya_kislota_date', 'skf_date', 'kreatinin_date', 'protein_date', 'urine_eritrocit_date',
                     'urine_leycocit_date',
                     'microalbumuria_date')
    def check_date_format(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            if parsed_date > datetime.now():
                raise ValidationException(message="Даты не могут быть позже текущего дня")
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
    return await hsn_command_block_laboratory_test_update(context)
