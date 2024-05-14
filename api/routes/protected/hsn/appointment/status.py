from core.hsn.appointment import hsn_get_appointment_status
from shared.db.models.appointment.appointment import AppointmentStatus
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@appointment_router.get(
    "/status/{patient_appointment_id}",
    response_model=AppointmentStatus,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Узнать статус приема по его id",
    tags=["Прием"]
)
async def get_appointment_status(request: Request, patient_appointment_id: int):
    doctor_id: int = request.user.doctor.id
    return await hsn_get_appointment_status(doctor_id,patient_appointment_id)
