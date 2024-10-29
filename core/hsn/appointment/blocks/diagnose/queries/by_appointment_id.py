from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from sqlalchemy import select, Select, Result


@SessionContext()
async def hsn_query_block_diagnose_by_appointment_id(
        appointment_id: int
) -> AppointmentDiagnoseBlock:
    query: Select = (
        select(AppointmentDBModel.block_diagnose_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    block_diagnose_id: int = cursor.scalar()
    if not block_diagnose_id:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block: Select = (
        select(AppointmentDiagnoseBlockDBModel)
        .where(AppointmentDiagnoseBlockDBModel.id == block_diagnose_id)
    )
    cursor: AsyncResult = await db_session.execute(query_get_block)
    block_diagnose: AppointmentDiagnoseBlockDBModel = cursor.scalars().first()
    return AppointmentDiagnoseBlock.model_validate(block_diagnose)
