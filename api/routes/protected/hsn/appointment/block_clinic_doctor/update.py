from typing import Optional

from domains.core.hsn.appointment.blocks.clinic_doctor import (
    HsnBlockClinicDoctorUpdateContext,
    hsn_block_clinic_doctor_update,
)
from domains.core.hsn.appointment.blocks.clinic_doctor.model import (
    DisabilityType,
    LgotaDrugsType,
    AppointmentClinicDoctorBlockResponse,
)
from .router import block_clinic_doctor_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from pydantic import BaseModel, Field
from fastapi import Request


class UpdateBlockClinicDoctorRequestBody(BaseModel):
    referring_doctor: Optional[str] = Field(None, max_length=500)
    referring_clinic_organization: Optional[str] = Field(None, max_length=500)
    disability: Optional[DisabilityType] = Field(DisabilityType.NO.value)
    lgota_drugs: Optional[LgotaDrugsType] = Field(LgotaDrugsType.NO.value)
    has_hospitalization: Optional[bool] = Field(False)
    count_hospitalization: Optional[int] = Field(None, gt=0)
    last_hospitalization_date: Optional[str] = Field(None)


@block_clinic_doctor_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentClinicDoctorBlockResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_block_clinic_doctor_route(
    request: Request, appointment_id: int, body: UpdateBlockClinicDoctorRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    doctor_id: int = request.user.doctor.id
    context = HsnBlockClinicDoctorUpdateContext(
        appointment_id=appointment_id, **body.model_dump()
    )
    return await hsn_block_clinic_doctor_update(doctor_id, context)
