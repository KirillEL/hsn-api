from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from shared.db.db_session import session
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_diagnose import (
    AppointmentDiagnoseBlockDBModel,
)
from sqlalchemy import select


async def hsn_get_block_diagnose_by_appointment_id(appointment_id: int):
    query = (
        select(AppointmentDBModel.block_diagnose_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await session.execute(query)
    block_diagnose_id = cursor.scalar()
    if block_diagnose_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = select(AppointmentDiagnoseBlockDBModel).where(
        AppointmentDiagnoseBlockDBModel.id == block_diagnose_id
    )
    cursor = await session.execute(query_get_block)
    block_diagnose = cursor.scalars().first()
    return AppointmentDiagnoseBlock.model_validate(block_diagnose)
