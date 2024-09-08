from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock, hsn_get_block_ekg_by_appointment_id
from .router import block_ekg_router
from fastapi import Request


@block_ekg_router.get(
    "/{appointment_id}",
    response_model=AppointmentEkgBlock,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_ekg_by_appointment_id(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_get_block_ekg_by_appointment_id(appointment_id)
