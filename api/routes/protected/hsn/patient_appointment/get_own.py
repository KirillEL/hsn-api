from .router import patient_appointment_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.patient_appointment import hsn_patient_appointment_get_by_doctor_id


@patient_appointment_router.get(
    "/{doctor_id}",
    response_model="",
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_appointment_get_by_doctor_id(doctor_id: int):
    return await hsn_patient_appointment_get_by_doctor_id(doctor_id)