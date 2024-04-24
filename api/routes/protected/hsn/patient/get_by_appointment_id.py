from core.hsn.patient import hsn_get_patient_by_appointment_id
from core.hsn.patient.model import PatientResponse, PatientResponseWithoutFullName
from .router import patient_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@patient_router.get(
    "/appointment/{appointment_id}",
    response_model=PatientResponseWithoutFullName,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_patient_by_appointment_id(request: Request, appointment_id: int):
    return await hsn_get_patient_by_appointment_id(appointment_id)