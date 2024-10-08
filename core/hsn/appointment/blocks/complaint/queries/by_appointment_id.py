from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from sqlalchemy import select

@SessionContext()
async def hsn_query_block_complaint_by_appointment_id(appointment_id:int):
    query = (
        select(AppointmentDBModel.block_complaint_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    block_complaint_id = cursor.scalar()
    if block_complaint_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = (
        select(AppointmentComplaintBlockDBModel)
        .where(AppointmentComplaintBlockDBModel.id == block_complaint_id)
    )
    cursor = await db_session.execute(query_get_block)
    block_complaint = cursor.scalars().first()
    return AppointmentComplaintBlock.model_validate(block_complaint)