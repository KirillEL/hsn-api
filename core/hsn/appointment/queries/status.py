from loguru import logger
from sqlalchemy import select, exc

from api.exceptions import InternalServerException, NotFoundException
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel, AppointmentStatus


@SessionContext()
async def hsn_get_appointment_status(doctor_id: int, patient_appointment_id: int):
    logger.info(f'hsn_get_appointment_status...')
    try:
        query = (
            select(AppointmentDBModel)
            .where(AppointmentDBModel.id == patient_appointment_id)
            .where(AppointmentDBModel.doctor_id == doctor_id)
        )
        cursor = await db_session.execute(query)
        appointment = cursor.scalars().first()
        if not appointment:
            raise NotFoundException(message="Прием не найден!")
        logger.info(f'status: {appointment.status}')
        return appointment.status
    except NotFoundException as ne:
        raise ne
    except exc.SQLAlchemyError as sqle:
        raise UnprocessableEntityException(message=str(sqle))
    except Exception as e:
        raise InternalServerException
