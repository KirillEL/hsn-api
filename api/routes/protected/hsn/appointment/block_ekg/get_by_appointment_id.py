from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.appointment.blocks.ekg import (
    AppointmentEkgBlock,
    hsn_query_block_ekg_by_appointment_id,
)
from core.hsn.appointment.blocks.ekg.model import AppointmentEkgBlockResponse
from .router import block_ekg_router
from fastapi import Request


@block_ekg_router.get(
    "/{appointment_id}",
    response_model=AppointmentEkgBlockResponse | None,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_ekg_by_appointment_id_route(request: Request, appointment_id: int):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_block_ekg_by_appointment_id(
        request.user.doctor.id, appointment_id
    )
