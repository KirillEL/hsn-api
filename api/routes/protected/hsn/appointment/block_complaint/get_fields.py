from core.hsn.appointment.blocks.complaint import hsn_get_block_complaint_fields
from core.hsn.appointment.blocks.complaint.model import AppointmentBlockBooleanFieldsResponse
from .router import block_complaint_router
from api.exceptions import ExceptionResponseSchema


@block_complaint_router.get(
    "/fields",
    response_model=list[AppointmentBlockBooleanFieldsResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_complaint_fields():
    return await hsn_get_block_complaint_fields()