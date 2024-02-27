from .router import patient_router
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from fastapi import Request, Response
from core.hsn.patient import Patient, HsnPatientCreateContext, hsn_patient_create
from api.exceptions import ExceptionResponseSchema
from shared.db.models.patient import LgotaDrugs, ClassificationFuncClasses, Disability


class CreatePatientRequest(BaseModel):
    name: str = Field(None, max_length=100)
    last_name: str = Field(None, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    age: int = Field(None, gt=0)
    gender: str = Field(..., max_length=1)
    height: int = Field(None, gt=0)
    main_diagnose: str = Field(None, max_length=5000)
    disability: str = Field(Disability.NO_DISABILITY.name)
    date_setup_diagnose: date = Field(...)
    school_hsn_date: date = Field(...)
    lgota_drugs: str = Field(LgotaDrugs.NO_LGOTA.name)
    note: str = Field(None, max_length=5000)
    has_chronic_heart: bool = Field(False)
    classification_func_classes: str = Field(ClassificationFuncClasses.FK1.name)
    has_stenocardia: bool = Field(False)
    has_arteria_hypertension: bool = Field(False)
    arteria_hypertension_age: int = Field(..., ge=0)
    # cabinet_id: int = Field(None, gt=0) # кабинет не нужен по идее так как кабинет берется от врача
    # врач создает пациента

    phone_number: int = Field(None, gt=0)
    snils: str = Field(None, max_length=16)
    address: str = Field(None, max_length=1000)
    mis_number: int = Field(None)
    date_birth: date = Field(...)
    relative_phone_number: int = Field(...)
    parent: str = Field(...)
    date_dead: Optional[date] = Field(None)


@patient_router.post(
    "/",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_create(request: Request, req_body: CreatePatientRequest):
    context = HsnPatientCreateContext(
        user_id=request.user.id,
        **req_body.dict()
    )
    return await hsn_patient_create(context)
