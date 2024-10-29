from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from sqlalchemy import select, Select, Result


@SessionContext()
async def hsn_query_block_laboratory_test_by_appointment_id(
        doctor_id: int,
        appointment_id: int
) -> AppointmentLaboratoryTestBlock:
    query: Select = (
        select(
            AppointmentDBModel.block_laboratory_test_id,
            AppointmentDBModel.doctor_id
        )
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    result = cursor.first()

    if not result:
        raise NotFoundException(message="Блок лабораторные тесты не найден")

    block_laboratory_test_id, appointment_doctor_id = result

    if appointment_doctor_id != doctor_id:
        raise ForbiddenException(message="У вас нет прав ")

    if not block_laboratory_test_id:
        raise NotFoundException(message="У приема нет данного блока")

    query_get_block: Select = (
        select(AppointmentLaboratoryTestBlockDBModel)
        .where(AppointmentLaboratoryTestBlockDBModel.id == block_laboratory_test_id)
    )
    cursor: AsyncResult = await db_session.execute(query_get_block)
    block_laboratory_test: AppointmentLaboratoryTestBlock = cursor.scalars().first()
    return AppointmentLaboratoryTestBlock.model_validate(block_laboratory_test)
