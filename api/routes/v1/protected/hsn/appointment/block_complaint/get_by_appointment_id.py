from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.complaint import (
    AppointmentComplaintBlock,
    hsn_get_block_complaint_by_appointment_id,
)
from core.hsn.appointment.blocks.complaint.model import AppointmentComplaintBlockResponse
from .router import block_complaint_router


@block_complaint_router.get(
    "/{appointment_id}",
    response_model=AppointmentComplaintBlockResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_complaint_by_appointment_id(appointment_id: int):
    return await hsn_get_block_complaint_by_appointment_id(appointment_id)
