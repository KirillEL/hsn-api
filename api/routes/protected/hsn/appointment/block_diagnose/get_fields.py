from typing import List

from domains.core.hsn.appointment.blocks.base_model import (
    AppointmentBlockBooleanTextFieldsResponse,
)
from domains.core.hsn.appointment.blocks.diagnose import hsn_query_block_diagnose_fields
from .router import block_diagnose_router
from api.exceptions import ExceptionResponseSchema


@block_diagnose_router.get(
    "/fields",
    response_model=List[AppointmentBlockBooleanTextFieldsResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_diagnose_fields():
    return await hsn_query_block_diagnose_fields()
