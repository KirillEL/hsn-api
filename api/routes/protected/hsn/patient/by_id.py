from .router import patient_router
from api.exceptions import ExceptionResponseSchema

from .schemas import PatientResponse


@patient_router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_patient_by_id(patient_id: int):
    pass