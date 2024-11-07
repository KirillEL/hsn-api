from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from sqlalchemy import select, Select, Result, Row

from shared.db.queries import db_query_entity_by_id


@SessionContext()
async def hsn_query_block_ekg_by_appointment_id(
        doctor_id: int,
        appointment_id: int
) -> AppointmentEkgBlock | None:
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(appointment_id))

    query: Select = (
        select(AppointmentDBModel.block_ekg_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_ekg_id = cursor.scalar()

    if not block_ekg_id:
        return None

    query_get_block: Select = (
        select(AppointmentEkgBlockDBModel)
        .where(AppointmentEkgBlockDBModel.id == block_ekg_id)
    )
    cursor: Result = await db_session.execute(query_get_block)
    block_ekg: AppointmentEkgBlockDBModel = cursor.scalars().first()
    return AppointmentEkgBlock.model_validate(block_ekg)
