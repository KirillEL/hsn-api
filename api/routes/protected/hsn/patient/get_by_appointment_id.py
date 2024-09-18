from core.hsn.patient import hsn_query_patient_by_appointment_id
from core.hsn.patient.model import PatientResponse, PatientWithoutFullNameResponse
from .router import patient_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from fastapi import Request


@patient_router.get(
    "/appointment/{appointment_id}",
    response_model=PatientWithoutFullNameResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_patient_by_appointment_id(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_patient_by_appointment_id(appointment_id)
