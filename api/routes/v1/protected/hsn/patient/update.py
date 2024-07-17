from datetime import datetime

from loguru import logger

from core.hsn.appointment.blocks.clinic_doctor.model import DisabilityType
from core.hsn.patient.schemas import PatientResponse
from core.hsn.patient.queries.own import GenderType, LocationType, LgotaDrugsType
from .router import patient_router
from api.exceptions import ExceptionResponseSchema, ValidationException
from core.hsn.patient import Patient, hsn_update_patient_by_id, HsnPatientUpdateContext
from fastapi import Request
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional
import re


class UpdatePatientRequestBody(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    patronymic: Optional[str] = Field(None, max_length=255)
    gender: Optional[GenderType] = Field(GenderType.MALE)
    birth_date: Optional[str] = Field(None)
    dod: Optional[str] = Field(None)
    location: Optional[LocationType] = Field(LocationType.NSK.value)
    district: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    clinic: Optional[str] = Field(None)
    referring_doctor: Optional[str] = Field(None)
    referring_clinic_organization: Optional[str] = Field(None)
    disability: Optional[DisabilityType] = Field(None)
    lgota_drugs: Optional[LgotaDrugsType] = Field(None)
    has_hospitalization: Optional[bool] = Field(None)
    count_hospitalization: Optional[int] = Field(None)
    last_hospitalization_date: Optional[str] = Field(None)
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


@patient_router.patch(
    "/{patient_id}",
    response_model=PatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def update_patient_by_id(request: Request, patient_id: int, body: UpdatePatientRequestBody):
    context = HsnPatientUpdateContext(
        user_id=request.user.id,
        patient_id=patient_id,
        **body.model_dump()
    )
    return await hsn_update_patient_by_id(context)