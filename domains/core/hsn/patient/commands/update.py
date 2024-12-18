from sqlalchemy import update, select
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException
from domains.core.hsn.patient.commands.create import convert_to_patient_response
from domains.core.hsn.patient.model import PatientResponse
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models import ContragentDBModel
from domains.shared.db.models.patient import PatientDBModel
from pydantic import BaseModel, Field
from typing import Optional
from utils import contragent_hasher


class HsnCommandPatientUpdateContext(BaseModel):
    doctor_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)

    name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    dod: Optional[str] = None
    location: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    clinic: Optional[str] = None
    referring_doctor: Optional[str] = Field(None)
    referring_clinic_organization: Optional[str] = Field(None)
    disability: Optional[str] = None
    lgota_drugs: Optional[str] = None
    has_hospitalization: Optional[bool] = None
    count_hospitalization: Optional[int] = Field(None)
    last_hospitalization_date: Optional[str] = None
    patient_note: Optional[str] = None


class ContragentUpdateContext(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    birth_date: Optional[str] = None
    dod: Optional[str] = None


async def check_patient_exists_by_id(patient_id: int):
    query = select(PatientDBModel).where(PatientDBModel.id == patient_id)
    cursor = await db_session.execute(query)
    patient = cursor.scalars().first()
    if patient is None:
        raise NotFoundException(message="Пациент с таким id не найден!")


@SessionContext()
async def hsn_command_patient_update_by_id(context: HsnCommandPatientUpdateContext):
    await check_patient_exists_by_id(context.patient_id)
    patient_update_values = {
        key: value
        for key, value in context.dict().items()
        if key in PatientDBModel.__table__.columns and value is not None
    }
    if patient_update_values:
        await db_session.execute(
            update(PatientDBModel)
            .values(**patient_update_values, editor_id=context.doctor_id)
            .where(PatientDBModel.id == context.patient_id)
        )

    query_get_patient_contragent_id = select(PatientDBModel.contragent_id).where(
        PatientDBModel.id == context.patient_id
    )
    cursor = await db_session.execute(query_get_patient_contragent_id)
    contragent_id = cursor.scalar()

    contragent_update_values = {
        key: contragent_hasher.encrypt(value)
        for key, value in context.dict().items()
        if key in ContragentDBModel.__table__.columns and value is not None
    }
    if contragent_update_values:
        await db_session.execute(
            update(ContragentDBModel)
            .values(**contragent_update_values)
            .where(ContragentDBModel.id == contragent_id)
        )

    await db_session.commit()

    result = await db_session.execute(
        select(PatientDBModel)
        .options(selectinload(PatientDBModel.contragent))
        .where(PatientDBModel.id == context.patient_id)
    )
    updated_patient = result.scalars().first()
    if updated_patient:
        converted_patient = await convert_to_patient_response(updated_patient)
        return PatientResponse.model_validate(converted_patient)
