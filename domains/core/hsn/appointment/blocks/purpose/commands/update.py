from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import select, update, exc, insert
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import ForbiddenException
from domains.core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from domains.core.hsn.appointment.blocks.purpose.model import (
    MedicinePrescriptionUpdateSchema,
)
from domains.shared.db.models import MedicinesPrescriptionDBModel
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from domains.shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.queries import db_query_entity_by_id


class HsnAppointmentPurposeUpdateContext(BaseModel):
    doctor_id: int = Field(gt=0)
    appointment_id: int = Field(gt=0)

    medicine_prescriptions: list[MedicinePrescriptionUpdateSchema]


async def update_medicine_prescription(
    med_prescription_id: int, editor_id: int, data: MedicinePrescriptionUpdateSchema
) -> None:
    query = (
        update(MedicinesPrescriptionDBModel)
        .values(id=med_prescription_id, editor_id=editor_id, **data.model_dump())
        .where(MedicinesPrescriptionDBModel.id == med_prescription_id)
    )
    try:
        await db_session.execute(query)
        await db_session.commit()
    except exc.SQLAlchemyError as sqle:
        logger.error(f"Failed to update med_prescription: {str(sqle)}")
        raise InternalServerException


async def create_medicine_prescription(
    appointment_purpose_id: int, doctor_id: int, data: MedicinePrescriptionUpdateSchema
) -> None:
    query = insert(MedicinesPrescriptionDBModel).values(
        appointment_purpose_id=appointment_purpose_id,
        drug_id=data.drug_id,
        dosa=data.dosa,
        note=data.note or "",
        author_id=doctor_id,
    )
    try:
        await db_session.execute(query)
        await db_session.commit()
    except exc.SQLAlchemyError as sqle:
        logger.error(f"Failed to create med_prescription: {str(sqle)}")
        raise InternalServerException


@SessionContext()
async def hsn_appointment_purpose_update(context: HsnAppointmentPurposeUpdateContext):
    appointment = await db_query_entity_by_id(
        AppointmentDBModel, context.appointment_id
    )
    if not appointment:
        raise NotFoundException(
            message="Прием c id:{} не найден".format(context.appointment_id)
        )

    if appointment.doctor_id != context.doctor_id:
        raise ForbiddenException(
            "У вас нет прав для доступа к приему с id:{}".format(context.appointment_id)
        )

    query_get_appointment_purpose = select(AppointmentPurposeDBModel.id).where(
        AppointmentPurposeDBModel.is_deleted.is_(False),
        AppointmentPurposeDBModel.appointment_id == context.appointment_id,
    )

    cursor = await db_session.execute(query_get_appointment_purpose)
    purpose_id = cursor.scalar()

    if not purpose_id:
        raise NotFoundException

    for m_d in context.medicine_prescriptions:
        query = select(MedicinesPrescriptionDBModel).where(
            MedicinesPrescriptionDBModel.is_deleted.is_(False),
            MedicinesPrescriptionDBModel.drug_id == m_d.drug_id,
        )
        cursor = await db_session.execute(query)
        med_prescription = cursor.scalars().first()
        if med_prescription:
            await update_medicine_prescription(
                med_prescription_id=med_prescription.id,
                editor_id=context.doctor_id,
                data=MedicinePrescriptionUpdateSchema(
                    drug_id=m_d.drug_id, dosa=m_d.dosa, note=m_d.note or ""
                ),
            )
        else:
            await create_medicine_prescription(
                appointment_purpose_id=purpose_id,
                doctor_id=context.doctor_id,
                data=MedicinePrescriptionUpdateSchema(
                    drug_id=m_d.drug_id, dosa=m_d.dosa, note=m_d.note or ""
                ),
            )

    query_get_updated_block = (
        select(AppointmentPurposeDBModel)
        .where(
            AppointmentPurposeDBModel.is_deleted.is_(False),
            AppointmentPurposeDBModel.id == purpose_id,
        )
        .options(
            selectinload(AppointmentPurposeDBModel.medicine_prescriptions).selectinload(
                MedicinesPrescriptionDBModel.drug
            )
        )
    )
    cursor = await db_session.execute(query_get_updated_block)
    updated_appointment_purpose_block = cursor.scalars().first()

    return AppointmentPurposeFlat.model_validate(updated_appointment_purpose_block)
