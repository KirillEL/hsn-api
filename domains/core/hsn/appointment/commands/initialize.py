from typing import Optional

from sqlalchemy.sql.dml import ReturningInsert

from api.exceptions import NotFoundException
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models.patient import PatientDBModel
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from sqlalchemy import insert, select, Result
from pydantic import BaseModel, Field


class HsnCommandAppointmentInitContext(BaseModel):
    user_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    patient_id: int
    date: Optional[str] = Field(None)
    date_next: Optional[str] = Field(None)


async def check_patient_exists(patient_id: int):
    query = select(PatientDBModel).where(PatientDBModel.id == patient_id)
    cursor = await db_session.execute(query)
    patient = cursor.scalars().first()
    if patient is None:
        raise NotFoundException(message="Пациент не найден!")


@SessionContext()
async def hsn_command_appointment_initialize(
    context: HsnCommandAppointmentInitContext,
) -> int:
    payload = context.model_dump(exclude={"user_id"}, exclude_none=True)
    await check_patient_exists(context.patient_id)

    query: ReturningInsert = (
        insert(AppointmentDBModel)
        .values(**payload, author_id=context.doctor_id)
        .returning(AppointmentDBModel.id)
    )
    cursor: Result = await db_session.execute(query)
    await db_session.commit()
    new_patient_appointment_id: int = cursor.scalar()
    return new_patient_appointment_id
