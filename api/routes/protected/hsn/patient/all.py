from .router import patient_router
from .schemas import PatientResponse
from api.exceptions import ExceptionResponseSchema
from typing import List, Optional
from core.hsn.patient.model import Patient
from core.hsn.patient import hsn_patient_list


@patient_router.get(
    "/",
    response_model=List[Patient],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_list(limit: int = None, offset: int = None, pattern: str = None):
    return await hsn_patient_list(limit, offset, pattern)
