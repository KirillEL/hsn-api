from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import joinedload, contains_eager, selectinload

from api.exceptions import NotFoundException, BadRequestException, ValidationException
from core.hsn.appointment import Appointment
from core.hsn.appointment.model import PatientAppointmentFlat
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field, ValidationError

from shared.db.models.appointment.purpose import AppointmentPurposeDBModel


class HsnAppointmentListContext(BaseModel):
    user_id: int = Field(gt=0)

    limit: Optional[int] = None
    offset: Optional[int] = None


@SessionContext()
async def hsn_appointment_list(context: HsnAppointmentListContext):
    try:
        logger.info("Получение списка приемов...")
        # Создаем базовый запрос
        query = select(AppointmentDBModel).where(AppointmentDBModel.is_deleted.is_(False),
                                                 AppointmentDBModel.doctor_id == context.user_id)

        query = query.outerjoin(AppointmentDBModel.block_clinic_doctor) \
            .outerjoin(AppointmentDBModel.block_clinical_condition) \
            .outerjoin(AppointmentDBModel.block_diagnose) \
            .outerjoin(AppointmentDBModel.block_ekg) \
            .outerjoin(AppointmentDBModel.block_complaint) \
            .outerjoin(AppointmentDBModel.block_laboratory_test) \
            .outerjoin(AppointmentDBModel.purposes)

        query = query.options(selectinload(AppointmentDBModel.block_clinic_doctor),
                              selectinload(AppointmentDBModel.block_clinical_condition),
                              selectinload(AppointmentDBModel.block_diagnose),
                              selectinload(AppointmentDBModel.block_ekg),
                              selectinload(AppointmentDBModel.block_complaint),
                              selectinload(AppointmentDBModel.block_laboratory_test),
                              selectinload(AppointmentDBModel.purposes).selectinload(
                                  AppointmentPurposeDBModel.medicine_prescription))

        if context.limit is not None:
            query = query.limit(context.limit)
        if context.offset is not None:
            query = query.offset(context.offset)

        cursor = await db_session.execute(query)
        patient_appointments = cursor.unique().scalars().all()

        return [PatientAppointmentFlat.model_validate(p_a) for p_a in patient_appointments]
    except ValidationError as ve:
        logger.error(f'Ошибка валидации приемов: {ve}')
        raise ValidationException()
    except Exception as e:
        logger.error(f'Ошибка при получении всех приемов: {e}')
        raise BadRequestException()
