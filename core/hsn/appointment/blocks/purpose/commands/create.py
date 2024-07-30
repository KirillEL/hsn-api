from loguru import logger
from sqlalchemy.orm import joinedload

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from shared.db import Transaction
from shared.db.db_session import session
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import insert, select, exc

from shared.db.models import MedicinesPrescriptionDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.transaction import Propagation


class MedicineContext(BaseModel):
    medicine_prescription_id: int = Field(gt=0)
    dosa: str
    note: Optional[str] = None


class HsnAppointmentPurposeCreateContext(BaseModel):
    user_id: int = Field(gt=0)
    appointment_id: int
    medicine_prescriptions: list[MedicineContext]


async def check_appointment_exists(appointment_id: int):
    query = select(AppointmentDBModel).where(AppointmentDBModel.id == appointment_id)
    cursor = await session.execute(query)
    appointment = cursor.scalars().first()
    if appointment is None:
        raise NotFoundException(message="Такого приема не существует!")


async def check_medicine_prescription_exists(medicine_prescription_id: int):
    query = select(MedicinesPrescriptionDBModel).where(
        MedicinesPrescriptionDBModel.id == medicine_prescription_id
    )
    cursor = await session.execute(query)
    medicine_prescription = cursor.scalars().first()
    if medicine_prescription is None:
        raise NotFoundException(message="Такого препарата не найдено!")


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_appointment_purpose_create(context: HsnAppointmentPurposeCreateContext):
    await check_appointment_exists(context.appointment_id)
    for med_prescription in context.medicine_prescriptions:
        await check_medicine_prescription_exists(
            med_prescription.medicine_prescription_id
        )
    payload = context.model_dump(exclude={"user_id"})
    appointment_id = context.appointment_id
    created_purposes = []
    for med_prescription in context.medicine_prescriptions:
        query = (
            insert(AppointmentPurposeDBModel)
            .values(
                author_id=context.user_id,
                appointment_id=appointment_id,
                **med_prescription.model_dump()
            )
            .returning(AppointmentPurposeDBModel.id)
        )
        cursor = await session.execute(query)
        inserted_id = cursor.scalar()

        select_query = (
            select(AppointmentPurposeDBModel)
            .options(
                joinedload(AppointmentPurposeDBModel.medicine_prescription).joinedload(
                    MedicinesPrescriptionDBModel.medicine_group
                )
            )
            .where(AppointmentPurposeDBModel.id == inserted_id)
        )
        cursor = await session.execute(select_query)
        created_purpose = cursor.scalar_one()
        created_purposes.append(created_purpose)

    return [AppointmentPurposeFlat.model_validate(p) for p in created_purposes]
