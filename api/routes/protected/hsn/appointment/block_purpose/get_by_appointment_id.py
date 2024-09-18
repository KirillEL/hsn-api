from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat, hsn_query_purposes_by_appointment_id
from core.hsn.appointment.blocks.purpose.model import AppointmentPurposeResponseFlat
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from fastapi import Request


@block_purpose_router.get(
    "/{appointment_id}",
    response_model=dict,
    responses={'400': {"model": ExceptionResponseSchema}}
)
async def get_purposes_by_appointment_id(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_purposes_by_appointment_id(appointment_id)
