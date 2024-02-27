from datetime import date
from typing import Optional

from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import select, insert, update
from pydantic import BaseModel, Field
from fastapi import Request


class PatientUpdateDto(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[str] = Field(..., max_length=1)
    height: Optional[int] = Field(None, gt=0)
    main_diagnose: Optional[str] = Field(None, max_length=5000)
    disability: Optional[str] = Field("")
    date_setup_diagnose: Optional[date] = Field(...)
    school_hsn_date: Optional[date] = Field(...)
    lgota_drugs: Optional[str] = Field("")
    note: Optional[str] = Field(None, max_length=5000)
    has_chronic_heart: Optional[bool] = Field(False)
    classification_func_classes: Optional[str] = Field("")
    has_stenocardia: Optional[bool] = Field(False)
    has_arteria_hypertension: Optional[bool] = Field(False)
    arteria_hypertension_age: Optional[int]= Field(..., ge=0)
    cabinet_id: Optional[int] = Field(None, gt=0)  # кабинет не нужен по идее так как кабинет берется от врача

    phone_number: Optional[int] = Field(None, gt=0)
    snils: Optional[str] = Field(None, max_length=16)
    address: Optional[str] = Field(None, max_length=1000)
    mis_number: Optional[int] = Field(None)
    date_birth: date = Field(...)
    relative_phone_number: Optional[int] = Field(...)
    parent: Optional[str] = Field(...)
    date_dead: Optional[date] = Field(None)


@admin_patient_router.put(
    "/patients/{patient_id}",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_update(patient_id: int, request: Request, dto: PatientUpdateDto):
    query = (
        update(PatientDBModel)
        .values(
            **dto,
            editor_id=request.user.id
        )
        .where(PatientDBModel.id == patient_id)
        .returning(PatientDBModel)
    )
    cursor = await db_session.execute(query)
    updated_patient = cursor.scalars().first()

    return Patient.model_validate(updated_patient)