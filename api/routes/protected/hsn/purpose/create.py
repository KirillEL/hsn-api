from core.hsn.medicine_prescription import MedicinePrescription
from .router import purpose_router
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from typing import Optional
from core.hsn.purpose import AppointmentPurposeFlat, hsn_appointment_purpose_create, HsnAppointmentPurposeCreateContext
from fastapi import Request

class MedicineData(BaseModel):
    medicine_prescription_id: int = Field(gt=0)
    dosa: str = Field(max_length=1000)
    note: Optional[str] = Field(None)



class CreateAppointmentPurposeRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    medicine_prescriptions: list[MedicineData]



@purpose_router.post(
    "",
    response_model=list[AppointmentPurposeFlat],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_appointment_purpose(request: Request, body: CreateAppointmentPurposeRequestBody):
    context = HsnAppointmentPurposeCreateContext(
        user_id=request.user.id,
        **body.model_dump()
    )
    return await hsn_appointment_purpose_create(context)