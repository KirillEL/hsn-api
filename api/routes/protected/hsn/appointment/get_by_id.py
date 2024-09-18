from core.hsn.appointment import Appointment, hsn_appointment_by_id
from core.hsn.appointment.model import PatientAppointmentFlat
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from fastapi import Request, status


@appointment_router.get(
    "/{appointment_id}",
    response_model=PatientAppointmentFlat,
    responses={"400": {"model": ExceptionResponseSchema}},
    tags=["Прием"],
    summary="Получение приема по id"
)
async def get_appointment_by_id(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_appointment_by_id(doctor_id=request.user.doctor.id, appointment_id=appointment_id)
