from api.exceptions import NotFoundException, InternalServerException
from core.hsn.purpose import AppointmentPurposeFlat
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import insert, select

from shared.db.models import MedicinesPrescriptionDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel


class HsnAppointmentPurposeCreateContext(BaseModel):
    user_id: int = Field(gt=0)
    appointment_id: int
    medicine_prescription_id: int
    note: Optional[str] = None
    dosa: str

async def check_appointment_exists(appointment_id: int):
    query = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    appointment = cursor.scalars().first()
    if appointment is None:
        raise NotFoundException(message="Такого приема не существует!")


async def check_medicine_prescription_exists(medicine_prescription_id: int):
    query = (
        select(MedicinesPrescriptionDBModel)
        .where(MedicinesPrescriptionDBModel.id == medicine_prescription_id)
    )
    cursor = await db_session.execute(query)
    medicine_prescription = cursor.scalars().first()
    if medicine_prescription is None:
        raise NotFoundException(message="Такого препарата не найдено!")

@SessionContext()
async def hsn_appointment_purpose_create(context: HsnAppointmentPurposeCreateContext):
    try:
        await check_appointment_exists(context.appointment_id)
        await check_medicine_prescription_exists(context.medicine_prescription_id)
        payload = context.model_dump(exclude={'user_id'})
        query = (
            insert(AppointmentPurposeDBModel)
            .values(
                author_id=context.user_id,
                **payload
            )
            .returning(AppointmentPurposeDBModel)
        )
        cursor = await db_session.execute(query)
        await db_session.commit()
        new_appointment_purpose = cursor.scalars().first()

        return AppointmentPurposeFlat.model_validate(new_appointment_purpose)
    except NotFoundException as ne:
        await db_session.rollback()
        raise ne