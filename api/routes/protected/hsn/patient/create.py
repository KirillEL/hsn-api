from .router import patient_router
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from fastapi import Request, Response
from core.hsn.patient import Patient, HsnPatientCreateContext, hsn_patient_create
from api.exceptions import ExceptionResponseSchema


class CreatePatientRequest(BaseModel):
    user_id: int = Field(None, gt=0)

    name: str = Field(None, max_length=100)
    last_name: str = Field(None, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    age: int = Field(None, gt=0)
    gender: str = Field(..., max_length=1)

    phone_number: int = Field(None, gt=0)
    snils: str = Field(None, max_length=16)
    address: str = Field(None, max_length=1000)


@patient_router.post(
    "/",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_create(request: Request, req_body: CreatePatientRequest):
    context = HsnPatientCreateContext(user_id=request.user.id, **req_body)
    return await hsn_patient_create(context)
