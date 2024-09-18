from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import select, update, exc
from sqlalchemy.orm import selectinload

from core.hsn.appointment.blocks.clinic_doctor.commands.create import check_appointment_exists
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from core.hsn.appointment.blocks.purpose.model import MedicinePrescriptionData
from shared.db.models import MedicinesPrescriptionDBModel
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from shared.db.db_session import db_session, SessionContext


class HsnAppointmentPurposeUpdateContext(BaseModel):
    doctor_id: int = Field(gt=0)
    appointment_id: int = Field(gt=0)

    medicine_prescriptions: list[MedicinePrescriptionData]


@SessionContext()
async def hsn_appointment_purpose_update(context: HsnAppointmentPurposeUpdateContext):
    # Exclude doctor_id and appointment_id from payload
    await check_appointment_exists(context.appointment_id)
    query_get_appointment_purpose = (
        select(AppointmentPurposeDBModel.id)
        .where(AppointmentPurposeDBModel.is_deleted.is_(False),
               AppointmentPurposeDBModel.appointment_id == context.appointment_id)
    )

    cursor = await db_session.execute(query_get_appointment_purpose)
    purpose_id = cursor.scalar()

    if purpose_id:
        for prescription in context.medicine_prescriptions:
            query_update = (
                update(MedicinesPrescriptionDBModel)
                .values(
                    editor_id=context.doctor_id,
                    **prescription.model_dump()
                )
                .where(MedicinesPrescriptionDBModel.id == prescription.id)
            )
            await db_session.execute(query_update)

        await db_session.commit()

    query = (
        select(AppointmentPurposeDBModel)
        .where(AppointmentPurposeDBModel.is_deleted.is_(False),
               AppointmentPurposeDBModel.appointment_id == context.appointment_id)
        .options(
            selectinload(AppointmentPurposeDBModel.medicine_prescriptions)
            .selectinload(MedicinesPrescriptionDBModel.drug)
        )
    )
    cursor = await db_session.execute(query)
    updated_appointment_purpose_block = cursor.scalars().first()

    return AppointmentPurposeFlat.model_validate(updated_appointment_purpose_block)
