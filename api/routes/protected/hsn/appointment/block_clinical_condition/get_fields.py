from typing import List

from core.hsn.appointment.blocks.clinical_condition import (
    hsn_query_block_clinical_condition_fields,
)
from core.hsn.appointment.blocks.complaint.model import (
    AppointmentBlockBooleanFieldsResponse,
)
from .router import block_clinical_condition_router
from api.exceptions import ExceptionResponseSchema


@block_clinical_condition_router.get(
    "/fields",
    response_model=List[AppointmentBlockBooleanFieldsResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_clinical_condition_fields_route():
    return await hsn_query_block_clinical_condition_fields()
