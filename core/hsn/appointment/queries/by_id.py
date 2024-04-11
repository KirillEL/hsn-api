from loguru import logger
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, ValidationException, BadRequestException
from core.hsn.appointment.model import PatientAppointmentFlat
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_appointment_by_id(user_id: int, appointment_id: int):
    try:
        query = select(AppointmentDBModel).where(AppointmentDBModel.is_deleted.is_(False),
                                                 AppointmentDBModel.doctor_id == user_id,
                                                 AppointmentDBModel.id == appointment_id)

        query = query.outerjoin(AppointmentDBModel.block_clinic_doctor) \
            .outerjoin(AppointmentDBModel.block_clinical_condition) \
            .outerjoin(AppointmentDBModel.block_diagnose) \
            .outerjoin(AppointmentDBModel.block_ekg) \
            .outerjoin(AppointmentDBModel.block_complaint) \
            .outerjoin(AppointmentDBModel.block_laboratory_test)

        query = query.options(selectinload(AppointmentDBModel.block_clinic_doctor),
                              selectinload(AppointmentDBModel.block_clinical_condition),
                              selectinload(AppointmentDBModel.block_diagnose),
                              selectinload(AppointmentDBModel.block_ekg),
                              selectinload(AppointmentDBModel.block_complaint),
                              selectinload(AppointmentDBModel.block_laboratory_test))

        cursor = await db_session.execute(query)
        patient_appointment = cursor.scalars().first()
        if patient_appointment is None:
            raise NotFoundException(message="Прием не найден!")

        return PatientAppointmentFlat.model_validate(patient_appointment)
    except ValidationError as ve:
        logger.error(f'Ошибка валидации приема: {ve}')
        raise ValidationException()
    except Exception as e:
        logger.error(f'Возникла ошибка: {e}')
        raise e
