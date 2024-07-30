from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.laboratory_test import (
    AppointmentLaboratoryTestBlock,
    hsn_get_block_laboratory_test_by_appointment_id,
)
from .router import block_laboratory_test_router


@block_laboratory_test_router.get(
    "/{appointment_id}",
    response_model=AppointmentLaboratoryTestBlock,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_laboratory_test_by_appointment_id(appointment_id: int):
    return await hsn_get_block_laboratory_test_by_appointment_id(appointment_id)
