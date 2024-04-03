from core.hsn.appointment import Appointment, HsnCreatePatientAppontmentContext, hsn_patient_appontment_create
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as tdate


class AppointmentCreateRequestBody(BaseModel):
    doctor_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)
    date: tdate = Field(tdate.today())
    date_next: Optional[tdate] = Field(None)
    block_clinic_doctor_id: int = Field(gt=0)
    block_diagnose_id: int = Field(gt=0)
    block_laboratory_test_id: int = Field(gt=0)
    block_ekg_id: int = Field(gt=0)
    block_complaint_id: int = Field(gt=0)
    block_clinical_condition_id: int = Field(gt=0)


@appointment_router.post(
    "",
    response_model=Appointment,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Создать прием пациента",
    status_code=status.HTTP_201_CREATED,
    tags=["Прием"]
)
async def appointment_create(request: Request, body: AppointmentCreateRequestBody):
    context = HsnCreatePatientAppontmentContext(
        user_id=request.user.id,
        **body.model_dump()
    )
    return await hsn_patient_appontment_create(context)
