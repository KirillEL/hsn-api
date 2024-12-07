from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.complaint import (
    hsn_query_block_complaint_by_appointment_id,
)
from domains.core.hsn.appointment.blocks.complaint.model import (
    AppointmentComplaintBlockResponse,
)
from .router import block_complaint_router
from fastapi import Request


@block_complaint_router.get(
    "/{appointment_id}",
    response_model=AppointmentComplaintBlockResponse | None,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_complaint_by_appointment_id_route(
    request: Request, appointment_id: int
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    doctor_id: int = request.user.doctor.id
    return await hsn_query_block_complaint_by_appointment_id(doctor_id, appointment_id)
