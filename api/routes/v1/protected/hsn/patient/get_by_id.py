from core.hsn.patient import hsn_get_patient_by_id
from core.hsn.patient.schemas import PatientResponse, PatientResponseWithoutFullName
from .router import patient_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@patient_router.get(
    "/{patient_id}",
    response_model=PatientResponseWithoutFullName,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_patient_by_id(request: Request, patient_id: int):
    return await hsn_get_patient_by_id(request.user.id, patient_id)
