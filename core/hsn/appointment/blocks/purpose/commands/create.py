from loguru import logger

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import insert, select, exc, Result

from shared.db.models import MedicinesPrescriptionDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.queries import db_query_entity_by_id


class MedicineContext(BaseModel):
    dosa: str
    drug_id: int
    note: Optional[str] = None


class HsnAppointmentPurposeCreateContext(BaseModel):
    doctor_id: int = Field(gt=0)
    appointment_id: int
    medicine_prescriptions: list[MedicineContext]


async def check_medicine_prescription_exists(medicine_prescription_id: int):
    query = (
        select(MedicinesPrescriptionDBModel)
        .where(MedicinesPrescriptionDBModel.id == medicine_prescription_id)
    )
    cursor = await db_session.execute(query)
    medicine_prescription = cursor.scalars().first()
    if not medicine_prescription:
        raise NotFoundException(message="Такого препарата не найдено")


@SessionContext()
async def hsn_command_appointment_purpose_create(context: HsnAppointmentPurposeCreateContext):
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(context.appointment_id))

    if appointment.doctor_id != context.doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(context.appointment_id))

    query_create_purpose_block = (
        insert(AppointmentPurposeDBModel)
        .values(
            appointment_id=context.appointment_id,
            author_id=context.doctor_id
        )
        .returning(AppointmentPurposeDBModel.id)
    )
    cursor: Result = await db_session.execute(query_create_purpose_block)
    new_purpose_block_id = cursor.scalar()

    for med_prescription in context.medicine_prescriptions:
        query = (
            insert(MedicinesPrescriptionDBModel)
            .values(
                author_id=context.doctor_id,
                appointment_purpose_id=new_purpose_block_id,
                dosa=med_prescription.dosa,
                drug_id=med_prescription.drug_id,
                note=med_prescription.note
            )
        )
        await db_session.execute(query)

    await db_session.commit()

    return new_purpose_block_id
