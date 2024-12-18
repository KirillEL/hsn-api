from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.laboratory_test import (
    hsn_query_block_laboratory_test_by_appointment_id,
)
from domains.core.hsn.appointment.blocks.laboratory_test.model import (
    AppointmentLaboratoryTestBlockResponse,
)
from .router import block_laboratory_test_router
from fastapi import Request


@block_laboratory_test_router.get(
    "/{appointment_id}",
    response_model=AppointmentLaboratoryTestBlockResponse | None,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_laboratory_test_by_appointment_id_route(
    request: Request, appointment_id: int
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_block_laboratory_test_by_appointment_id(
        request.user.doctor.id, appointment_id
    )
