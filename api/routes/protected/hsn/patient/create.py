from datetime import date as tdate, datetime
from typing import Optional
from fastapi import Request, status

from core.hsn.patient.model import PatientFlat
from core.hsn.patient.queries.own import GenderType, LgotaDrugsType
from shared.db.models.patient import PatientDBModel
from sqlalchemy import insert
from shared.db.db_session import db_session
from .router import patient_router
from core.hsn.patient import Patient, HsnPatientCreateContext, hsn_patient_create
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field


class CreatePatientRequestBody(BaseModel):
    name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    patronymic: Optional[str] = Field(None, max_length=255)
    gender: GenderType = Field(GenderType.MALE)
    height: float = Field(..., gt=0)
    age: int = Field(..., gt=0, le=100)
    date_setup_diagnose: tdate = Field(...)
    lgota_drugs: LgotaDrugsType = Field(LgotaDrugsType.NO)

    phone_number: int = Field(gt=0)
    snils: str = Field(...)
    address: str = Field(...)
    mis_number: int = Field(gt=0)
    date_birth: tdate = Field()
    relative_phone_number: Optional[int] = Field(None, gt=0)
    parent: Optional[str] = Field(None, max_length=500)
    date_dead: Optional[tdate] = Field(None)

    note: Optional[str] = Field(None, max_length=1000)


class PatientResponse(BaseModel):
    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None


@patient_router.post(
    "",
    response_model=PatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Создание нового пациента",
    status_code=status.HTTP_201_CREATED
)
async def patient_create(request: Request, body: CreatePatientRequestBody):
    context = HsnPatientCreateContext(**body.dict(), cabinet_id=request.user.doctor.cabinet_id,
                                      user_id=request.user.doctor.id)
    new_patient = await hsn_patient_create(context)
    return new_patient
