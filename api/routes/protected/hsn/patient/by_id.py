from .router import patient_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.patient.model import Patient
from core.hsn.patient import hsn_patient_by_id


@patient_router.get(
    "/{patient_id}",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_by_id(patient_id: int):
    return await hsn_patient_by_id(patient_id)
