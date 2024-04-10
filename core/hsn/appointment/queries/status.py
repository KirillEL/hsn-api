from loguru import logger
from sqlalchemy import select, exc

from api.exceptions import InternalServerException, NotFoundException
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel, AppointmentStatus


@SessionContext()
async def hsn_get_appointment_status(patient_appointment_id: int):
    try:
        query = (
            select(AppointmentDBModel)
            .where(AppointmentDBModel.id == patient_appointment_id)
        )
        cursor = await db_session.execute(query)
        appointment = cursor.scalars().first()
        if appointment is None:
            raise NotFoundException(message="Прием не найден!")
        logger.info(f'status: {appointment.status}')
        return appointment.status
    except NotFoundException as ne:
        logger.error(f'NotFoundError')
        raise ne
    except exc.SQLAlchemyError as sqle:
        logger.error(f'sqlalchemyError: {sqle}')
        raise UnprocessableEntityException
    except Exception as e:
        logger.error(f'server_error: {e}')
        raise InternalServerException
