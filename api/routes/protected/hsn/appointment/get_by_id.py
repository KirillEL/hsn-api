from core.hsn.patient_appointment import PatientAppointment, hsn_appointment_by_id
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, status


@appointment_router.get(
    "/{appointment_id}",
    response_model=PatientAppointment,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_appointment_by_id(appointment_id: int):
    return await hsn_appointment_by_id(appointment_id)