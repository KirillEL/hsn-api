from typing import Optional

from loguru import logger
from sqlalchemy import select

from api.exceptions import NotFoundException, BadRequestException, ValidationException
from core.hsn.appointment import PatientAppointment
from core.hsn.appointment.model import PatientAppointmentFlat
from shared.db.models.patient_appointment import PatientAppointmentsDBModel
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field, ValidationError


class HsnAppointmentListContext(BaseModel):
    user_id: int = Field(gt=0)

    limit: Optional[int] = None
    offset: Optional[int] = None


@SessionContext()
async def hsn_appointment_list(context: HsnAppointmentListContext):
    try:
        logger.info("Получение списка приемов...")
        query = (
            select(PatientAppointmentsDBModel)
            .where(PatientAppointmentsDBModel.is_deleted.is_(False))
            .where(PatientAppointmentsDBModel.doctor_id == context.user_id)
        )

        if context.limit is not None:
            query = query.limit(context.limit)

        if context.offset is not None:
            query = query.offset(context.offset)

        cursor = await db_session.execute(query)
        patient_appointments = cursor.scalars().all()

        return [PatientAppointmentFlat.model_validate(p_a) for p_a in patient_appointments]
    except ValidationError as ve:
        logger.error(f'Ошибка валидации приемов: {ve}')
        raise ValidationException()
    except Exception as e:
        logger.error(f'Ошибка при получение всех приемов: {e}')
        raise BadRequestException()

