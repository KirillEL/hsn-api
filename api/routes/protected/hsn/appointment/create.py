from core.hsn.appointment import PatientAppointment
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, status
from pydantic import BaseModel, Field
from typing import Optional

class AppointmentCreateRequestBody(BaseModel):
    pass


@appointment_router.post(
    "",
    response_model=PatientAppointment,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Создать прием пациента",
    status_code=status.HTTP_201_CREATED
)
async def appointment_create(request: Request, body: AppointmentCreateRequestBody):
    pass