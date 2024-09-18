from typing import List

from core.hsn.appointment.blocks.base_model import AppointmentBlockTextDateFieldsResponse, \
    AppointmentBlockTextDateLaboratoryTestFieldsResponse
from core.hsn.appointment.blocks.laboratory_test import hsn_query_block_laboratory_test_fields
from .router import block_laboratory_test_router
from api.exceptions import ExceptionResponseSchema


@block_laboratory_test_router.get(
    "/fields",
    response_model=AppointmentBlockTextDateLaboratoryTestFieldsResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_laboratory_test_fields():
    return await hsn_query_block_laboratory_test_fields()