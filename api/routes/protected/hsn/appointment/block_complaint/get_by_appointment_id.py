from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock, hsn_get_block_complaint_by_appointment_id
from .router import block_complaint_router
from fastapi import Request


@block_complaint_router.get(
    "/{appointment_id}",
    response_model=AppointmentComplaintBlock,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_complaint_by_appointment_id(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_get_block_complaint_by_appointment_id(appointment_id)
