from datetime import date as tdate, datetime
from typing import Optional
import re
from fastapi import Request, status
from loguru import logger

from core.hsn.appointment.blocks.clinic_doctor.model import DisabilityType
from core.hsn.patient.schemas import PatientFlat, PatientResponse
from core.hsn.patient.queries.own import GenderType, LgotaDrugsType, LocationType
from shared.db.models.patient import PatientDBModel
from sqlalchemy import insert
from .router import patient_router
from core.hsn.patient import Patient, HsnPatientCreateContext, hsn_patient_create
from api.exceptions import ExceptionResponseSchema, ValidationException
from pydantic import BaseModel, Field, validator, field_validator, model_validator


class CreatePatientRequestBody(BaseModel):
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    patronymic: Optional[str] = Field(None, max_length=255)
    gender: GenderType = Field(GenderType.MALE)
    birth_date: str = Field(default=datetime.today().strftime("%d.%m.%Y"))
    dod: Optional[str] = Field(None)
    location: LocationType = Field(default=LocationType.NSK)
    district: str = Field(max_length=255)
    address: str = Field(max_length=255)
    phone: str
    clinic: str
    referring_doctor: Optional[str] = Field(None)
    referring_clinic_organization: Optional[str] = Field(None)
    disability: DisabilityType = Field(DisabilityType.NO.value)
    lgota_drugs: LgotaDrugsType = Field(LgotaDrugsType.NO.value)
    has_hospitalization: bool
    count_hospitalization: Optional[int] = Field(None)
    last_hospitalization_date: Optional[str] = Field(default=datetime.today().strftime("%d.%m.%Y"))
    patient_note: Optional[str] = Field(None, max_length=1000)

    @field_validator("birth_date", "dod")
    def date_format_validation(cls, v):
        if v is not None:
            try:
                parsed_date = datetime.strptime(v, "%d.%m.%Y")
            except ValueError:
                raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")
            if cls.__fields__.get('last_hospitalization_date') and parsed_date > datetime.now():
                raise ValidationException(message="Дата последней госпитализации не должна быть позже чем текущая дата")
        return v

    @field_validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValidationException(message="Номер телефона не валидный!")
        return v

    @model_validator(mode="after")
    def validate_birth_date(self):
        birth_date = datetime.strptime(self.birth_date, "%d.%m.%Y")
        current_date = datetime.now()
        age = (current_date - birth_date).days / 365.25
        logger.debug(f'age: {age}')
        if age < 0:
            raise ValidationException(message="Дата рождения не должна быть в будущем.")
        if age > 110:
            raise ValidationException(message="Возраст не должен превышать 110 лет.")
        return self

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