from datetime import date
from typing import Optional
from sqlalchemy.orm import joinedload
from shared.db.models import ContragentDBModel
from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import select, insert
from pydantic import BaseModel, Field
from fastapi import Request


class PatientCreateDto(BaseModel):
    name: str = Field(None, max_length=100)
    last_name: str = Field(None, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    age: int = Field(None, gt=0)
    gender: str = Field("")
    height: int = Field(None, gt=0)
    main_diagnose: str = Field(None, max_length=5000)
    disability: str = Field("")
    date_setup_diagnose: date = Field(...)
    school_hsn_date: date = Field(...)
    lgota_drugs: str = Field("")
    note: str = Field(None, max_length=5000)
    has_chronic_heart: bool = Field(False)
    classification_func_classes: str = Field("")
    has_stenocardia: bool = Field(False)
    has_arteria_hypertension: bool = Field(False)
    arteria_hypertension_age: int = Field(..., ge=0)
    cabinet_id: int = Field(None, gt=0)


    phone_number: str = Field(None)
    snils: str = Field(None, max_length=16)
    address: str = Field(None, max_length=1000)
    mis_number: str = Field(None)
    date_birth: str = Field(...)
    relative_phone_number: str = Field(...)
    parent: str = Field(...)
    date_dead: Optional[str] = Field(None)


@admin_patient_router.post(
    "/patients",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_create(request: Request, dto: PatientCreateDto):
    contragent_dto = dto.model_dump(exclude={
        'name',
        'last_name',
        'patronymic',
        'age',
        'gender',
        'height',
        'main_diagnose',
        'disability',
        'date_setup_diagnose',
        'school_hsn_date',
        'lgota_drugs',
        'note',
        'has_chronic_heart',
        'classification_func_classes',
        'has_stenocardia',
        'has_arteria_hypertension',
        'arteria_hypertension_age',
        'cabinet_id'
    })
    patient_dto = dto.model_dump(exclude={
        "phone_number",
        "snils",
        "address",
        "mis_number",
        "date_birth",
        "relative_phone_number",
        "parent",
        "date_dead",
    })
    from utils import contragent_hasher
    query_contragent = (
        insert(ContragentDBModel)
        .values(
            phone_number=contragent_hasher.encrypt(value=contragent_dto.get('phone_number')),
            snils=contragent_hasher.encrypt(value=contragent_dto.get('snils')),
            address=contragent_hasher.encrypt(value=contragent_dto.get('address')),
            mis_number=contragent_hasher.encrypt(value=contragent_dto.get('mis_number')),
            date_birth=contragent_hasher.encrypt(value=contragent_dto.get('date_birth')),
            relative_phone_number=contragent_hasher.encrypt(value=contragent_dto.get('relative_phone_number')),
            parent=contragent_hasher.encrypt(value=contragent_dto.get('parent')),
            date_dead=contragent_hasher.encrypt(value=contragent_dto.get('date_dead'))
        )
        .returning(ContragentDBModel.id)
    )
    cursor = await db_session.execute(query_contragent)
    await db_session.commit()
    new_contragent_id = cursor.scalar()

    query = (
        insert(PatientDBModel)
        .values(
            **patient_dto,
            contragent_id=new_contragent_id,
            author_id=request.user.id
        )
        .returning(PatientDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_patient_id = cursor.scalar()

    query_get_new_patient = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.contragent))
        .where(PatientDBModel.id == new_patient_id)
    )
    cursor = await db_session.execute(query_get_new_patient)
    new_patient = cursor.scalars().first()
    new_patient.contragent.phone_number = contragent_hasher.decrypt(new_patient.contragent.phone_number)
    new_patient.contragent.snils = contragent_hasher.decrypt(new_patient.contragent.snils)
    new_patient.contragent.address = contragent_hasher.decrypt(new_patient.contragent.address)
    new_patient.contragent.mis_number = contragent_hasher.decrypt(new_patient.contragent.mis_number)
    new_patient.contragent.date_birth = contragent_hasher.decrypt(new_patient.contragent.date_birth)
    new_patient.contragent.relative_phone_number = contragent_hasher.decrypt(new_patient.contragent.relative_phone_number)
    new_patient.contragent.parent = contragent_hasher.decrypt(new_patient.contragent.parent)
    new_patient.contragent.date_dead = contragent_hasher.decrypt(new_patient.contragent.date_dead)

    return Patient.model_validate(new_patient)




