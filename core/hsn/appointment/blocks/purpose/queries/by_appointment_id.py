from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_get_purposes_by_appointment_id(appointment_id: int):
    query = (
        select(AppointmentPurposeDBModel)
        .options(selectinload(AppointmentPurposeDBModel.medicine_prescription))
        .where(AppointmentPurposeDBModel.appointment_id == appointment_id)
        .where(AppointmentPurposeDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    purposes = cursor.scalars().all()

    return [AppointmentPurposeFlat.model_validate(p) for p in purposes]
