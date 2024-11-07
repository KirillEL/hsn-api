from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from sqlalchemy import select, Result, Select

from shared.db.queries import db_query_entity_by_id


@SessionContext()
async def hsn_query_block_clinical_condition_by_appointment_id(
        doctor_id: int,
        appointment_id: int
) -> AppointmentClinicalConditionBlock | None:
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)
    if not appointment:
        raise NotFoundException(
            message="Прием с id: {} не найден".format(appointment_id)
        )

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            message="У вас нет прав для доступа к приему с id: {}".format(appointment_id)
        )

    query: Select = (
        select(AppointmentDBModel.block_clinical_condition_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query)

    block_clinical_condition_id: int = cursor.scalar()

    if not block_clinical_condition_id:
        return None

    query_get_block: Select = (
        select(AppointmentClinicalConditionBlockDBModel)
        .where(AppointmentClinicalConditionBlockDBModel.id == block_clinical_condition_id)
    )
    cursor: Result = await db_session.execute(query_get_block)
    block_clinical_condition: AppointmentClinicalConditionBlockDBModel = cursor.scalars().first()
    return AppointmentClinicalConditionBlock.model_validate(block_clinical_condition)
