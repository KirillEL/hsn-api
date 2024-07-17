from loguru import logger
from sqlalchemy import select, exc

from api.decorators import HandleExceptions
from api.exceptions import InternalServerException, NotFoundException
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import session
from shared.db.models.appointment.appointment import AppointmentDBModel, AppointmentStatus


async def hsn_get_appointment_status(doctor_id: int, patient_appointment_id: int):
    query = (
        select(AppointmentDBModel.status)
        .where(AppointmentDBModel.id == patient_appointment_id)
        .where(AppointmentDBModel.doctor_id == doctor_id)
    )
    cursor = await session.execute(query)
    appointment_status = cursor.scalar_one_or_none()
    if not appointment_status:
        raise NotFoundException(message="Прием не найден!")
    return appointment_status
