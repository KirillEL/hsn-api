from .router import purpose_router
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from typing import Optional
from core.hsn.purpose import AppointmentPurposeFlat, hsn_appointment_purpose_create, HsnAppointmentPurposeCreateContext
from fastapi import Request



class CreateAppointmentPurposeRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    medicine_prescription_id: int = Field(gt=0)
    dosa: str = Field(max_length=100)
    note: Optional[str] = Field(None)


@purpose_router.post(
    "",
    response_model=AppointmentPurposeFlat,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_appointment_purpose(request: Request, body: CreateAppointmentPurposeRequestBody):
    context = HsnAppointmentPurposeCreateContext(
        user_id=request.user.id,
        **body.model_dump()
    )
    return await hsn_appointment_purpose_create(context)