from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock, hsn_query_block_diagnose_by_appointment_id
from .router import block_diagnose_router
from fastapi import Request


@block_diagnose_router.get(
    "/{appointment_id}",
    response_model=AppointmentDiagnoseBlock,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_diagnose_by_appointment_id_route(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_block_diagnose_by_appointment_id(appointment_id)
