from datetime import date as tdate, datetime
from typing import Optional
from fastapi import Request, status

from core.hsn.appointment.blocks.clinic_doctor.model import DisabilityType
from core.hsn.patient.model import PatientFlat, PatientResponse
from core.hsn.patient.queries.own import GenderType, LgotaDrugsType, LocationType
from shared.db.models.patient import PatientDBModel
from sqlalchemy import insert
from shared.db.db_session import db_session
from .router import patient_router
from core.hsn.patient import Patient, HsnPatientCreateContext, hsn_patient_create
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field


class CreatePatientRequestBody(BaseModel):
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    patronymic: Optional[str] = Field(max_length=255)
    gender: GenderType = Field(GenderType.MALE)
    birth_date: tdate = Field(default=tdate.today())
    dod: Optional[tdate] = Field(default=None)
    location: LocationType = Field(default=LocationType.NSK.value)
    district: str = Field(max_length=255)
    address: str = Field(max_length=255)
    phone: int = Field(gt=0)
    clinic: str
    patient_note: Optional[str] = Field(max_length=1000)
    referring_doctor: Optional[str] = Field(max_length=255)
    referring_clinic_organization: Optional[str] = Field(max_length=255)
    disability: Optional[DisabilityType] = Field(DisabilityType.NO.value)
    lgota_drugs: Optional[LgotaDrugsType] = Field(LgotaDrugsType.NO.value)
    has_hospitalization: bool
    count_hospitalization: Optional[int] = Field(0)
    last_hospitalization_date: Optional[tdate] = Field(None)





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
