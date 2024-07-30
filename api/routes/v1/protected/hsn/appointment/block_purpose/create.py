from typing import Optional, List

from pydantic import Field, BaseModel
from fastapi import Request
from starlette import status

from core.hsn.appointment.blocks.purpose import (
    AppointmentPurposeFlat,
    HsnAppointmentPurposeCreateContext,
    hsn_appointment_purpose_create,
)
from core.hsn.appointment.blocks.purpose.model import AppointmentPurposeFlatResponse
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema


class MedicineData(BaseModel):
    medicine_prescription_id: int = Field(gt=0)
    dosa: str = Field(max_length=1000)
    note: Optional[str] = Field(None)


class CreateAppointmentPurposeRequest(BaseModel):
    appointment_id: int = Field(gt=0)
    medicine_prescriptions: list[MedicineData]


@block_purpose_router.post(
    "/create",
    response_model=List[AppointmentPurposeFlatResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment_purpose(
        request: Request, body: CreateAppointmentPurposeRequest
):
    context = HsnAppointmentPurposeCreateContext(
        user_id=request.user.id, **body.model_dump()
    )
    return await hsn_appointment_purpose_create(context)
