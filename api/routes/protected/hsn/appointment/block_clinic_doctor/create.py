from typing import Optional

from api.exceptions import (
    ExceptionResponseSchema,
    DoctorNotAssignedException,
    ValidationException,
)
from domains.core.hsn.appointment.blocks.clinic_doctor.model import (
    DisabilityType,
    LgotaDrugsType,
)
from .router import block_clinic_doctor_router
from domains.core.hsn.appointment.blocks.clinic_doctor import (
    hsn_command_appointment_block_clinic_doctor_create,
    HsnCommandAppointmentBlockClinicDoctorCreateContext,
)
from pydantic import BaseModel, Field, field_validator
from datetime import date as tdate, datetime
from fastapi import Request


class CreateBlockClinicDoctorRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    referring_doctor: Optional[str] = Field(None, max_length=500)
    referring_clinic_organization: Optional[str] = Field(None, max_length=500)
    disability: DisabilityType = Field(DisabilityType.NO.value)
    lgota_drugs: LgotaDrugsType = Field(LgotaDrugsType.NO.value)
    has_hospitalization: bool = Field(False)
    count_hospitalization: Optional[int] = Field(None, gt=0)
    last_hospitalization_date: Optional[tdate] = Field(None)

    @field_validator("last_hospitalization_date")
    def check_date_format(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")


@block_clinic_doctor_router.post(
    "/create", response_model=int, responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_clinic_doctor_route(
    request: Request, body: CreateBlockClinicDoctorRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentBlockClinicDoctorCreateContext(**body.model_dump())
    doctor_id: int = request.user.doctor.id
    return await hsn_command_appointment_block_clinic_doctor_create(doctor_id, context)
