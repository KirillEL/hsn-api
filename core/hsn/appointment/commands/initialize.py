from typing import Optional

from loguru import logger

from api.decorators import HandleExceptions
from api.exceptions import InternalServerException, NotFoundException
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from sqlalchemy import insert, exc, select
from pydantic import BaseModel, ConfigDict, Field


class HsnInitializeAppointmentContext(BaseModel):
    user_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    patient_id: int
    date: Optional[str] = Field(None)
    date_next: Optional[str] = Field(None)


async def check_patient_exists(patient_id: int):
    query = (
        select(PatientDBModel)
        .where(PatientDBModel.id == patient_id)
    )
    cursor = await db_session.execute(query)
    patient = cursor.scalars().first()
    if patient is None:
        raise NotFoundException(message="Пациент не найден!")


@SessionContext()
async def hsn_appointment_initialize(context: HsnInitializeAppointmentContext):
    payload = context.model_dump(exclude={'user_id'}, exclude_none=True)
    await check_patient_exists(context.patient_id)
    query = (
        insert(AppointmentDBModel)
        .values(
            **payload,
            author_id=context.doctor_id
        )
        .returning(AppointmentDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_patient_appointment_id = cursor.scalar()
    return new_patient_appointment_id
