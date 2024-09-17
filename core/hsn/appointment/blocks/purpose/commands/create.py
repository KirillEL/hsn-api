from loguru import logger
from sqlalchemy.orm import joinedload

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import insert, select, exc

from shared.db.models import MedicinesPrescriptionDBModel, MedicinesGroupDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel


class MedicineContext(BaseModel):
    dosa: str
    medicine_group_id: int
    note: Optional[str] = None


class HsnAppointmentPurposeCreateContext(BaseModel):
    doctor_id: int = Field(gt=0)
    appointment_id: int
    medicine_prescriptions: list[MedicineContext]


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
    await check_appointment_exists(context.appointment_id)

    payload = context.model_dump(exclude={'doctor_id'})
    appointment_id = context.appointment_id
    created_purposes = []

    # create appointment_purpose
    query_create_purpose_block = (
        insert(AppointmentPurposeDBModel)
        .values(
            appointment_id=context.appointment_id,
            author_id=context.doctor_id
        )
        .returning(AppointmentPurposeDBModel.id)
    )
    cursor = await db_session.execute(query_create_purpose_block)
    new_purpose_block_id = cursor.scalar()

    for med_prescription in context.medicine_prescriptions:
        logger.debug(f'med_prescription: {med_prescription}')
        query_select_med_group = (
            select(MedicinesGroupDBModel.id)
            .where(MedicinesGroupDBModel.is_deleted.is_(False),
                   MedicinesGroupDBModel.id == med_prescription.medicine_group_id)
        )
        cursor = await db_session.execute(query_select_med_group)
        med_group_id = cursor.scalar()

        query = (
            insert(MedicinesPrescriptionDBModel)
            .values(
                author_id=context.doctor_id,
                appointment_purpose_id=new_purpose_block_id,
                dosa=med_prescription.dosa,
                medicine_group_id=med_group_id
            )
        )
        await db_session.execute(query)

    await db_session.commit()

    return new_purpose_block_id
