from .router import patient_appointment_router
from api.exceptions import ExceptionResponseSchema


@patient_appointment_router.delete(
    "/{patient_appointment_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_patient_appointment_delete(patient_appointment_id: int):
    pass