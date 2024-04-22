from typing import Optional

from pydantic import Field, BaseModel
from fastapi import Request
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat, HsnAppointmentPurposeCreateContext, hsn_appointment_purpose_create
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema


class MedicineData(BaseModel):
    medicine_prescription_id: int = Field(gt=0)
    dosa: str = Field(max_length=1000)
    note: Optional[str] = Field(None)



class CreateAppointmentPurposeRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    medicine_prescriptions: list[MedicineData]



@block_purpose_router.post(
    "/create",
    response_model=list[AppointmentPurposeFlat],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_appointment_purpose(request: Request, body: CreateAppointmentPurposeRequestBody):
    context = HsnAppointmentPurposeCreateContext(
        user_id=request.user.id,
        **body.model_dump()
    )
    return await hsn_appointment_purpose_create(context)