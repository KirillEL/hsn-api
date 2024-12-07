from datetime import datetime
from typing import Optional
import re
from fastapi import Request, status
from loguru import logger

from api.exceptions.base import ValidationErrorTelegramSendMessageSchema
from tg_api import tg_bot
from domains.core.hsn.appointment.blocks.clinic_doctor.model import DisabilityType
from domains.core.hsn.patient.model import PatientResponse
from domains.core.hsn.patient.queries.own import GenderType, LgotaDrugsType, LocationType
from .router import patient_router
from domains.core.hsn.patient import HsnPatientCreateContext, hsn_patient_create
from api.exceptions import ExceptionResponseSchema, ValidationException
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)


class CreatePatientRequest(BaseModel):
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
    clinic: Optional[str] = Field(None, max_length=255)
    referring_doctor: Optional[str] = Field(None)
    referring_clinic_organization: Optional[str] = Field(None)
    disability: DisabilityType = Field(DisabilityType.NO.value)
    lgota_drugs: LgotaDrugsType = Field(LgotaDrugsType.NO.value)
    has_hospitalization: bool
    count_hospitalization: Optional[int] = Field(None)
    last_hospitalization_date: Optional[str] = Field(
        default=datetime.today().strftime("%d.%m.%Y")
    )
    patient_note: Optional[str] = Field(None, max_length=1000)


class ModelValidator(CreatePatientRequest):
    @field_validator("birth_date", "dod")
    def date_format_validation(cls, v):
        if v is not None:
            try:
                parsed_date = datetime.strptime(v, "%d.%m.%Y")
            except ValueError:
                raise ValidationException(
                    message="Дата должна быть в формате ДД.ММ.ГГГГ"
                )
            if (
                cls.__fields__.get("last_hospitalization_date")
                and parsed_date > datetime.now()
            ):
                raise ValidationException(
                    message="Дата последней госпитализации не должна быть позже чем текущая дата"
                )
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
        if age < 0:
            raise ValidationException(message="Дата рождения не должна быть в будущем.")
        if age > 100:
            raise ValidationException(message="Возраст не должен превышать 100 лет.")
        return self


@patient_router.post(
    "",
    response_model=PatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Создание нового пациента",
    status_code=status.HTTP_201_CREATED,
)
async def patient_create_route(request: Request, body: CreatePatientRequest):
    try:
        validated_body = ModelValidator.model_validate(body.model_dump())
        context = HsnPatientCreateContext(
            **validated_body.model_dump(),
            cabinet_id=request.user.doctor.cabinet_id,
            doctor_id=request.user.doctor.id
        )
        new_patient = await hsn_patient_create(context)
        return new_patient
    except ValidationException as ve:
        message_model = ValidationErrorTelegramSendMessageSchema(
            message="*Ошибка при создании пациента*",
            doctor_id=request.user.doctor.id,
            doctor_name=request.user.doctor.name,
            doctor_last_name=request.user.doctor.last_name,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            description=str(ve.message),
        )
        logger.error(str(message_model))
        tg_bot.send_message(message=str(message_model))
        raise ve
