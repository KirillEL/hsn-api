from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.patient.model import PatientAppointmentHistoryResponse
from core.hsn.patient.queries.history_appointment import hsn_query_patient_history_appointments
from .router import patient_router
from pydantic import BaseModel
from fastapi import Request
from fastapi import Path


@patient_router.get(
    "/history/{patient_id}/appointments",
    response_model=list[PatientAppointmentHistoryResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_patient_appointment_history(
        request: Request,
        patient_id: int = Path(..., gt=0)
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    doctor_id: int = request.user.doctor.id
    histories = await hsn_query_patient_history_appointments(
        doctor_id,
        patient_id
    )
    return [PatientAppointmentHistoryResponse.model_validate(model) for model in histories]

