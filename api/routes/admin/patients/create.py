from datetime import date
from typing import Optional

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
    gender: str = Field(..., max_length=1)
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
    cabinet_id: int = Field(None, gt=0)  # кабинет не нужен по идее так как кабинет берется от врача

    phone_number: int = Field(None, gt=0)
    snils: str = Field(None, max_length=16)
    address: str = Field(None, max_length=1000)
    mis_number: int = Field(None)
    date_birth: date = Field(...)
    relative_phone_number: int = Field(...)
    parent: str = Field(...)
    date_dead: Optional[date] = Field(None)


@admin_patient_router.post(
    "/patients",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_create(request: Request, dto: PatientCreateDto):
    query = (
        insert(PatientDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(PatientDBModel)
    )
    cursor = await db_session.execute(query)
    new_patient = cursor.scalars().first()

    return Patient.model_validate(new_patient)
