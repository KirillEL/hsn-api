from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from sqlalchemy import select, Select, Result

from shared.db.queries import db_query_entity_by_id


@SessionContext()
async def hsn_query_block_complaint_by_appointment_id(
        doctor_id: int,
        appointment_id: int
) -> AppointmentComplaintBlock | None:
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(appointment_id))

    query: Select = (
        select(AppointmentDBModel.block_complaint_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_complaint_id: int = cursor.scalar()

    if not block_complaint_id:
        return None

    query_get_block: Select = (
        select(AppointmentComplaintBlockDBModel)
        .where(AppointmentComplaintBlockDBModel.id == block_complaint_id)
    )
    cursor: Result = await db_session.execute(query_get_block)
    block_complaint: AppointmentComplaintBlockDBModel = cursor.scalars().first()
    return AppointmentComplaintBlock.model_validate(block_complaint)
