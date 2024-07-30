from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
    hsn_get_block_clinical_condition_by_appointment_id,
)
from .router import block_clinical_condition_router


@block_clinical_condition_router.get(
    "/{appointment_id}",
    response_model=AppointmentClinicalConditionBlock,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_clinical_condition_by_appointment_id(appointment_id: int):
    return await hsn_get_block_clinical_condition_by_appointment_id(appointment_id)
