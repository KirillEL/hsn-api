from core.hsn.patient import hsn_query_patient_by_id
from core.hsn.patient.model import PatientResponse, PatientWithoutFullNameResponse
from .router import patient_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from fastapi import Request


@patient_router.get(
    "/{patient_id}",
    response_model=PatientWithoutFullNameResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_patient_by_id_route(request: Request, patient_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_patient_by_id(request.user.doctor.id, patient_id)
