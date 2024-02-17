from .router import patient_appointment_router
from pydantic import BaseModel, Field
from typing import Optional
from api.exceptions import ExceptionResponseSchema

class CreatePatientAppointmentRequest(BaseModel):
    pass


@patient_appointment_router.post(
    "/",
    response_model="",
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_appointment_create():
    pass