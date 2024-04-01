from loguru import logger
from pydantic import ValidationError
from sqlalchemy import select

from api.exceptions import NotFoundException, ValidationException, BadRequestException
from core.hsn.appointment.model import PatientAppointmentFlat
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_appointment_by_id(appointment_id: int):
    try:
        query = (
            select(AppointmentDBModel)
            .where(AppointmentDBModel.is_deleted.is_(False))
            .where(AppointmentDBModel.id == appointment_id)
        )
        cursor = await db_session.execute(query)
        patient_appointment = cursor.scalars().first()
        if patient_appointment is None:
            raise NotFoundException()

        return PatientAppointmentFlat.model_validate(patient_appointment)
    except ValidationError as ve:
        logger.error(f'Ошибка валидации приема: {ve}')
        raise ValidationException()
    except Exception as e:
        logger.error(f'Возникла ошибка: {e}')
        raise e
