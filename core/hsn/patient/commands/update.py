from sqlalchemy import update, select
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, InternalServerException
from core.hsn.patient.commands.create import convert_to_patient_response
from core.hsn.patient.schemas import PatientResponse
from core.hsn.patient.queries.own import GenderType
from shared.db import Transaction
from shared.db.db_session import session
from shared.db.models import ContragentDBModel
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel, Field
from typing import Optional

from shared.db.transaction import Propagation
from utils import contragent_hasher


class HsnPatientUpdateContext(BaseModel):
    user_id: int = Field(gt=0)
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
    cursor = await session.execute(query)
    patient = cursor.scalars().first()
    if patient is None:
        raise NotFoundException(message="Пациент с таким id не найден!")


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_update_patient_by_id(context: HsnPatientUpdateContext):
    await check_patient_exists_by_id(context.patient_id)
    patient_update_values = {
        key: value
        for key, value in context.dict().items()
        if key in PatientDBModel.__table__.columns and value is not None
    }
    if patient_update_values:
        await session.execute(
            update(PatientDBModel)
            .values(**patient_update_values, editor_id=context.user_id)
            .where(PatientDBModel.id == context.patient_id)
        )

    query_get_patient_contragent_id = select(PatientDBModel.contragent_id).where(
        PatientDBModel.id == context.patient_id
    )
    cursor = await session.execute(query_get_patient_contragent_id)
    contragent_id = cursor.scalar()

    contragent_update_values = {
        key: contragent_hasher.encrypt(value)
        for key, value in context.dict().items()
        if key in ContragentDBModel.__table__.columns and value is not None
    }
    if contragent_update_values:
        await session.execute(
            update(ContragentDBModel)
            .values(**contragent_update_values)
            .where(ContragentDBModel.id == contragent_id)
        )

    result = await session.execute(
        select(PatientDBModel)
        .options(selectinload(PatientDBModel.contragent))
        .where(PatientDBModel.id == context.patient_id)
    )
    updated_patient = result.scalars().first()
    if updated_patient:
        converted_patient = await convert_to_patient_response(updated_patient)
        return PatientResponse.parse_obj(converted_patient)
