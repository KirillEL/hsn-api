from .router import patient_appointment_router
from pydantic import BaseModel, Field
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, Response


class UpdatePatientAppointmentRequest(BaseModel):
    pass


@patient_appointment_router.put(
    "/{patient_appointment_id}",
    response_model="",
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_appointment_update(patient_appointment_id: int, request: Request,
                                         req_body: UpdatePatientAppointmentRequest):
    pass

