from .router import patient_router
from .schemas import PatientResponse
from api.exceptions import ExceptionResponseSchema
from typing import List, Optional


@patient_router.get(
    "/",
    response_model=List[PatientResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_patients(limit: Optional[int] = None, offset: Optional[int] = None, pattern: Optional[str] = None):
    pass
