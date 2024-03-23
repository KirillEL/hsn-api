import datetime
from datetime import date as tdate
from typing import Optional

from fastapi import Request, Depends
from pydantic import BaseModel

from core.hsn.patient.model import Patient, PatientFlat
from core.hsn.patient.queries.own import hsn_get_own_patients, GenderType
from .router import patient_router
from api.exceptions import ExceptionResponseSchema


class GetOwnPatientsQueryParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    age: Optional[int] = None
    gender: Optional[GenderType] = GenderType.MALE
    dateBirth: Optional[tdate] = datetime.date.today()

class GetOwnPatientResponse(BaseModel):
    data: list[PatientFlat]
    total: int


@patient_router.get(
    '',
    response_model=GetOwnPatientResponse,
    responses={'400': {"model": ExceptionResponseSchema}},
    summary='Получить своих пациентов'
)
async def get_own_patients(request: Request, params: GetOwnPatientsQueryParams = Depends()):
    return await hsn_get_own_patients(request.user.id, **params.dict())
