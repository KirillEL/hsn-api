from typing import Optional

from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.clinic_doctor.model import DisabilityType, LgotaDrugsType
from .router import block_clinic_doctor_router
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock, hsn_appointment_block_clinic_doctor_create, HsnAppointmentBlockClinicDoctorCreateContext
from pydantic import BaseModel, Field
from datetime import date as tdate
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


@block_clinic_doctor_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_clinic_doctor(request: Request, body: CreateBlockClinicDoctorRequestBody):
    context = HsnAppointmentBlockClinicDoctorCreateContext(**body.model_dump())
    return await hsn_appointment_block_clinic_doctor_create(context)