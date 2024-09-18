from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from sqlalchemy import select


@SessionContext()
async def hsn_query_block_laboratory_test_by_appointment_id(appointment_id: int):
    query = (
        select(AppointmentDBModel.block_laboratory_test_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    block_laboratory_test_id = cursor.scalar()
    if block_laboratory_test_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = (
        select(AppointmentLaboratoryTestBlockDBModel)
        .where(AppointmentLaboratoryTestBlockDBModel.id == block_laboratory_test_id)
    )
    cursor = await db_session.execute(query_get_block)
    block_laboratory_test = cursor.scalars().first()
    return AppointmentLaboratoryTestBlock.model_validate(block_laboratory_test)
