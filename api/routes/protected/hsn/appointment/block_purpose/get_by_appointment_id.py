from domains.core.hsn.appointment.blocks.purpose import (
    hsn_query_purposes_by_appointment_id,
)
from .router import block_purpose_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from fastapi import Request


@block_purpose_router.get(
    "/{appointment_id}", responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_purposes_by_appointment_id_route(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    doctor_id: int = request.user.doctor.id
    return await hsn_query_purposes_by_appointment_id(doctor_id, appointment_id)
