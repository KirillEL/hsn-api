from domains.core.hsn.appointment.blocks.purpose import (
    HsnAppointmentPurposeUpdateContext,
    hsn_appointment_purpose_update,
    AppointmentPurposeFlat,
)
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Request


class UpdateMedicinePrescriptionModel(BaseModel):
    drug_id: Optional[int] = Field(None, gt=0)
    dosa: Optional[str] = Field(None, max_length=255)
    note: Optional[str] = Field(None, max_length=500)


class UpdateBlockPurposeRequestBody(BaseModel):
    medicine_prescriptions: list[UpdateMedicinePrescriptionModel]


@block_purpose_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentPurposeFlat,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_block_purpose_route(
    request: Request, appointment_id: int, body: UpdateBlockPurposeRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnAppointmentPurposeUpdateContext(
        doctor_id=request.user.doctor.id,
        appointment_id=appointment_id,
        medicine_prescriptions=body.medicine_prescriptions,
    )
    return await hsn_appointment_purpose_update(context)
