from datetime import date

from fastapi import Request
from pydantic import BaseModel

from core.hsn.patient.model import Patient, PatientFlat
from core.hsn.patient.queries.own import hsn_get_own_patients, GenderType
from .router import patient_router
from api.exceptions import ExceptionResponseSchema

class GetOwnPatientResponse(BaseModel):
    data: list[PatientFlat]
    total: int

@patient_router.get(
    '',
    response_model=GetOwnPatientResponse,
    responses={'400': {"model": ExceptionResponseSchema}}
)
async def get_own_patients(request: Request, limit: int = None, offset: int = None, age: int = None, gender: GenderType = None, dateBirth: date = None):
    return await hsn_get_own_patients(request.user.id, limit, offset, age, gender, dateBirth)
