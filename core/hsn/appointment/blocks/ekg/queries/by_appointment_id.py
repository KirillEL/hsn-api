from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from sqlalchemy import select, Select, Result, Row


@SessionContext()
async def hsn_query_block_ekg_by_appointment_id(
        doctor_id: int,
        appointment_id: int
) -> AppointmentEkgBlock:
    query: Select = (
        select(AppointmentDBModel.block_ekg_id, AppointmentDBModel.doctor_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    result = cursor.first()
    if not result:
        raise NotFoundException

    block_ekg_id, appointment_doctor_id = result

    if appointment_doctor_id != doctor_id:
        raise ForbiddenException

    if not block_ekg_id:
        raise NotFoundException(message="К приему пока не привязан данный блок")

    query_get_block: Select = (
        select(AppointmentEkgBlockDBModel)
        .where(AppointmentEkgBlockDBModel.id == block_ekg_id)
    )
    cursor: Result = await db_session.execute(query_get_block)
    block_ekg: AppointmentEkgBlockDBModel = cursor.scalars().first()
    return AppointmentEkgBlock.model_validate(block_ekg)
