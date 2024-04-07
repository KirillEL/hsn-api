from core.hsn.appointment.blocks.clinic_doctor.model import DisabilityType
from core.hsn.patient.model import PatientResponse
from core.hsn.patient.queries.own import GenderType, LocationType, LgotaDrugsType
from .router import patient_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.patient import Patient, hsn_update_patient_by_id, HsnPatientUpdateContext
from fastapi import Request
from pydantic import BaseModel, Field
from typing import Optional


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
    patient_note: Optional[str] = Field(None, max_length=1000)
    referring_doctor: Optional[str] = Field(None, max_length=255)
    referring_clinic_organization: Optional[str] = Field(None, max_length=255)
    disability: Optional[DisabilityType] = Field(DisabilityType.NO.value)
    lgota_drugs: Optional[LgotaDrugsType] = Field(LgotaDrugsType.NO.value)
    has_hospitalization: Optional[bool] = Field(False)
    last_hospitalization_date: Optional[str] = Field(None)


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
