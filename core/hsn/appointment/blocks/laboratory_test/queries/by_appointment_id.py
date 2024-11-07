from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from sqlalchemy import select, Select, Result

from shared.db.queries import db_query_entity_by_id


@SessionContext()
async def hsn_query_block_laboratory_test_by_appointment_id(
        doctor_id: int,
        appointment_id: int
) -> AppointmentLaboratoryTestBlock | None:
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(appointment_id))

    query: Select = (
        select(
            AppointmentDBModel.block_laboratory_test_id
        )
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_laboratory_test_id: int = cursor.scalar()

    if not block_laboratory_test_id:
        return None

    query_get_block: Select = (
        select(AppointmentLaboratoryTestBlockDBModel)
        .where(AppointmentLaboratoryTestBlockDBModel.id == block_laboratory_test_id)
    )
    cursor: AsyncResult = await db_session.execute(query_get_block)
    block_laboratory_test: AppointmentLaboratoryTestBlock = cursor.scalars().first()
    return AppointmentLaboratoryTestBlock.model_validate(block_laboratory_test)
