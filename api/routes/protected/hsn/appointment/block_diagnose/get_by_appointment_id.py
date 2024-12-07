from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.diagnose import (
    hsn_query_block_diagnose_by_appointment_id,
)
from domains.core.hsn.appointment.blocks.diagnose.model import AppointmentBlockDiagnoseResponse
from .router import block_diagnose_router
from fastapi import Request


@block_diagnose_router.get(
    "/{appointment_id}",
    response_model=AppointmentBlockDiagnoseResponse | None,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_diagnose_by_appointment_id_route(
    request: Request, appointment_id: int
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    doctor_id: int = request.user.doctor.id
    return await hsn_query_block_diagnose_by_appointment_id(doctor_id, appointment_id)
