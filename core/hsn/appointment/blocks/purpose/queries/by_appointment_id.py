from loguru import logger
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from core.hsn.appointment.blocks.purpose.commands.create import check_appointment_exists
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
@HandleExceptions()
async def hsn_get_purposes_by_appointment_id(appointment_id: int):
    await check_appointment_exists(appointment_id)
    query = (
        select(AppointmentPurposeDBModel)
        .options(selectinload(AppointmentPurposeDBModel.medicine_prescription))
        .where(AppointmentPurposeDBModel.appointment_id == appointment_id)
        .where(AppointmentPurposeDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    purposes = cursor.scalars().all()
    if len(purposes) == 0:
        raise NotFoundException(message="У приема нет блока назначений лекарственных препаратов")

    return [AppointmentPurposeFlat.model_validate(p) for p in purposes]
