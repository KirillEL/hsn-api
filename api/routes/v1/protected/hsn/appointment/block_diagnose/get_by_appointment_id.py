from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.diagnose import (
    AppointmentDiagnoseBlock,
    hsn_get_block_diagnose_by_appointment_id,
)
from core.hsn.appointment.blocks.diagnose.model import AppointmentDiagnoseBlockResponse
from .router import block_diagnose_router


@block_diagnose_router.get(
    "/{appointment_id}",
    response_model=AppointmentDiagnoseBlockResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_diagnose_by_appointment_id(appointment_id: int):
    return await hsn_get_block_diagnose_by_appointment_id(appointment_id)
