from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models.appointment.appointment import (
    AppointmentDBModel,
    AppointmentStatus,
)


@SessionContext()
async def hsn_query_appointment_status(
    doctor_id: int, patient_appointment_id: int
) -> AppointmentStatus:
    query: Select = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.id == patient_appointment_id)
        .where(AppointmentDBModel.doctor_id == doctor_id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    appointment: AppointmentDBModel = cursor.scalars().first()
    if not appointment:
        raise NotFoundException(message="Прием не найден!")
    return appointment.status
