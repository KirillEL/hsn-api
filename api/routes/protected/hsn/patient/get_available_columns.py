from core.hsn.patient import hsn_get_patient_available_columns
from core.hsn.patient.model import PatientAvailableColumnsResponse
from .router import patient_router
from api.exceptions import ExceptionResponseSchema


@patient_router.get(
    "/available_columns",
    response_model=list[PatientAvailableColumnsResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    response_model_exclude_none=True
)
async def get_patient_available_columns():
    return await hsn_get_patient_available_columns()