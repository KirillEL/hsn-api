from typing import Optional

from pydantic import Field, BaseModel
from fastapi import Request
from starlette import status

from domains.core.hsn.appointment.blocks.purpose import (
    HsnAppointmentPurposeCreateContext,
    hsn_command_appointment_purpose_create,
)
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException


class MedicineData(BaseModel):
    drug_id: int = Field(gt=0)
    dosa: str = Field(max_length=1000)
    note: Optional[str] = Field(None)


class CreateAppointmentPurposeRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    medicine_prescriptions: list[MedicineData]


@block_purpose_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment_purpose_route(
    request: Request, body: CreateAppointmentPurposeRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnAppointmentPurposeCreateContext(
        doctor_id=request.user.doctor.id, **body.model_dump()
    )
    return await hsn_command_appointment_purpose_create(context)
