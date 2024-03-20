from datetime import date

from fastapi import Request

from core.hsn.patient.model import Patient
from core.hsn.patient.queries.own import hsn_patient_own, GenderType
from .router import patient_router
from api.exceptions import ExceptionResponseSchema


@patient_router.get(
    '',
    response_model=list[Patient],
    responses={'400': {"model": ExceptionResponseSchema}}
)
async def get_own_patients(request: Request, limit: int = None, offset: int = None, age: int = None, gender: GenderType = None, dateBirth: date = None):
    return await hsn_patient_own(request.user.id, limit, offset, age, gender, dateBirth)
