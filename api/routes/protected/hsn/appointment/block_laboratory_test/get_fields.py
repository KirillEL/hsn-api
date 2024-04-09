from typing import List

from core.hsn.appointment.blocks.base_model import AppointmentBlockTextDateFieldsResponse
from core.hsn.appointment.blocks.laboratory_test import hsn_get_block_laboratory_test_fields
from .router import block_laboratory_test_router
from api.exceptions import ExceptionResponseSchema


@block_laboratory_test_router.get(
    "/fields",
    response_model=List[AppointmentBlockTextDateFieldsResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_laboratory_test_fields():
    return await hsn_get_block_laboratory_test_fields()