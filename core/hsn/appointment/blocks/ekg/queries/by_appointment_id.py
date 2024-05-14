from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from sqlalchemy import select


@SessionContext()
@HandleExceptions()
async def hsn_get_block_ekg_by_appointment_id(appointment_id: int):
    query = (
        select(AppointmentDBModel.block_ekg_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    block_ekg_id = cursor.scalar()
    if block_ekg_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = (
        select(AppointmentEkgBlockDBModel)
        .where(AppointmentEkgBlockDBModel.id == block_ekg_id)
    )
    cursor = await db_session.execute(query_get_block)
    block_ekg = cursor.scalars().first()
    return AppointmentEkgBlock.model_validate(block_ekg)
