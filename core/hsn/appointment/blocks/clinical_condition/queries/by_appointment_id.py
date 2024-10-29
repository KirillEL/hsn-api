from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from sqlalchemy import select, Result, Select


@SessionContext()
async def hsn_query_block_clinical_condition_by_appointment_id(
        appointment_id: int
) -> AppointmentClinicalConditionBlock:
    query: Select = (
        select(AppointmentDBModel.block_clinical_condition_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    block_clinical_condition_id: int = cursor.scalar()
    if not block_clinical_condition_id:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block: Select = (
        select(AppointmentClinicalConditionBlockDBModel)
        .where(AppointmentClinicalConditionBlockDBModel.id == block_clinical_condition_id)
    )
    cursor: AsyncResult = await db_session.execute(query_get_block)
    block_clinical_condition: AppointmentClinicalConditionBlockDBModel = cursor.scalars().first()
    return AppointmentClinicalConditionBlock.model_validate(block_clinical_condition)
