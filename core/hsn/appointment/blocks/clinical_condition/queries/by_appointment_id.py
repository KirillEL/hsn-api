from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock
from shared.db.db_session import session
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from sqlalchemy import select

async def hsn_get_block_clinical_condition_by_appointment_id(appointment_id:int):
    query = (
        select(AppointmentDBModel.block_clinical_condition_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await session.execute(query)
    block_clinical_condition_id = cursor.scalar()
    if block_clinical_condition_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = (
        select(AppointmentClinicalConditionBlockDBModel)
        .where(AppointmentClinicalConditionBlockDBModel.id == block_clinical_condition_id)
    )
    cursor = await session.execute(query_get_block)
    block_clinical_condition = cursor.scalars().first()
    return AppointmentClinicalConditionBlock.model_validate(block_clinical_condition)