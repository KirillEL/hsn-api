from loguru import logger
from sqlalchemy import select, exc

from api.exceptions import InternalServerException, NotFoundException
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel, AppointmentStatus


@SessionContext()
async def hsn_query_appointment_status(doctor_id: int, patient_appointment_id: int):
    query = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.id == patient_appointment_id)
        .where(AppointmentDBModel.doctor_id == doctor_id)
    )
    cursor = await db_session.execute(query)
    appointment = cursor.scalars().first()
    if not appointment:
        raise NotFoundException(message="Прием не найден!")
    return appointment.status
