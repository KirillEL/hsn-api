from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.laboratory_test import (
    AppointmentLaboratoryTestBlock,
    hsn_get_block_laboratory_test_by_appointment_id,
)
from core.hsn.appointment.blocks.laboratory_test.model import AppointmentLaboratoryTestBlockResponse
from .router import block_laboratory_test_router


@block_laboratory_test_router.get(
    "/{appointment_id}",
    response_model=AppointmentLaboratoryTestBlockResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_laboratory_test_by_appointment_id(appointment_id: int):
    return await hsn_get_block_laboratory_test_by_appointment_id(appointment_id)
