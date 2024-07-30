from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.ekg import (
    AppointmentEkgBlock,
    hsn_get_block_ekg_by_appointment_id,
)
from .router import block_ekg_router


@block_ekg_router.get(
    "/{appointment_id}",
    response_model=AppointmentEkgBlock,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_ekg_by_appointment_id(appointment_id: int):
    return await hsn_get_block_ekg_by_appointment_id(appointment_id)
