from core.hsn.appointment import Appointment, hsn_appointment_by_id
from core.hsn.appointment.model import PatientAppointmentFlat
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request, status


@appointment_router.get(
    "/{appointment_id}",
    response_model=PatientAppointmentFlat,
    responses={"400": {"model": ExceptionResponseSchema}},
    tags=["Прием"]
)
async def get_appointment_by_id(request: Request, appointment_id: int):
    doctor_id: int = request.user.doctor.id
    return await hsn_appointment_by_id(doctor_id, appointment_id)
