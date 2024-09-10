from datetime import datetime
from tg_api import tg_api
from loguru import logger

from core.hsn.appointment.blocks.clinic_doctor.model import DisabilityType
from core.hsn.patient.model import PatientResponse
from core.hsn.patient.queries.own import GenderType, LocationType, LgotaDrugsType
from . import ModelValidator
from .router import patient_router
from api.exceptions import ExceptionResponseSchema, ValidationException, DoctorNotAssignedException
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


@patient_router.patch(
    "/{patient_id}",
    response_model=PatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def update_patient_by_id(request: Request, patient_id: int, body: UpdatePatientRequestBody):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    try:
        validated_body = ModelValidator.model_validate(body.model_dump())
        context = HsnPatientUpdateContext(
            doctor_id=request.user.doctor.id,
            patient_id=patient_id,
            **validated_body.model_dump()
        )
        return await hsn_update_patient_by_id(context)
    except ValidationException as ve:
        logger.error(f"ValidationFailed: {ve.message}")
        error_message = (
            f"*Ошибка при получении списка пациентов*\n"
            f"Врач: *{request.user.doctor.name} {request.user.doctor.last_name}*\n"
            f"ID врача: {request.user.doctor.id}\n"
            f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Описание ошибки: `{str(ve.message)}`"
        )
        tg_api.send_telegram_message(
            message=error_message
        )
