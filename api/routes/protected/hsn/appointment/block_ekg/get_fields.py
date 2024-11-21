from typing import List

from core.hsn.appointment.blocks.complaint.model import (
    AppointmentBlockBooleanFieldsResponse,
    AppointmentBlockEkgBooleanFieldsResponse,
)
from core.hsn.appointment.blocks.ekg import hsn_query_block_ekg_fields
from .router import block_ekg_router
from api.exceptions import ExceptionResponseSchema


@block_ekg_router.get(
    "/fields",
    response_model=AppointmentBlockEkgBooleanFieldsResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_ekg_fields():
    return await hsn_query_block_ekg_fields()
