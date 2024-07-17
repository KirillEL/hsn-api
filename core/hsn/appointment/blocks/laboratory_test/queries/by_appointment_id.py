from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from shared.db.db_session import session
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from sqlalchemy import select


async def hsn_get_block_laboratory_test_by_appointment_id(appointment_id: int):
    query = (
        select(AppointmentDBModel.block_laboratory_test_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await session.execute(query)
    block_laboratory_test_id = cursor.scalar()
    if block_laboratory_test_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = (
        select(AppointmentLaboratoryTestBlockDBModel)
        .where(AppointmentLaboratoryTestBlockDBModel.id == block_laboratory_test_id)
    )
    cursor = await session.execute(query_get_block)
    block_laboratory_test = cursor.scalars().first()
    return AppointmentLaboratoryTestBlock.model_validate(block_laboratory_test)
