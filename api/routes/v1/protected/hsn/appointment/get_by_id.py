from core.hsn.appointment import hsn_appointment_by_id
from core.hsn.appointment.schemas import PatientAppointmentFlatResponse
from .router import appointment_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@appointment_router.get(
    "/{appointment_id}",
    response_model=PatientAppointmentFlatResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    tags=["Прием"],
    summary="Получение приема по id",
)
async def get_appointment_by_id(request: Request, appointment_id: int):
    doctor_id: int = request.user.doctor.id
    return await hsn_appointment_by_id(doctor_id, appointment_id)
