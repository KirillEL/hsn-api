from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat, hsn_get_purposes_by_appointment_id
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@block_purpose_router.get(
    "/{appointment_id}",
    response_model=list[AppointmentPurposeFlat],
    responses={'400': {"model": ExceptionResponseSchema}}
)
async def get_purposes_by_appointment_id(request: Request, appointment_id: int):
    return await hsn_get_purposes_by_appointment_id(appointment_id)