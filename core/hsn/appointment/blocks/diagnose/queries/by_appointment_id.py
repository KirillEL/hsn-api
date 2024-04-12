from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from sqlalchemy import select

@SessionContext()
async def hsn_get_block_diagnose_by_appointment_id(appointment_id:int):
    query = (
        select(AppointmentDBModel.block_diagnose_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    block_diagnose_id = cursor.scalar()
    if block_diagnose_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = (
        select(AppointmentDiagnoseBlockDBModel)
        .where(AppointmentDiagnoseBlockDBModel.id == block_diagnose_id)
    )
    cursor = await db_session.execute(query_get_block)
    block_diagnose = cursor.scalars().first()
    return AppointmentDiagnoseBlock.model_validate(block_diagnose)