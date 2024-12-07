from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.clinical_condition import (
    hsn_query_block_clinical_condition_by_appointment_id,
)
from domains.core.hsn.appointment.blocks.clinical_condition.model import (
    AppointmentClinicalConditionBlockResponse,
)
from .router import block_clinical_condition_router
from fastapi import Request


@block_clinical_condition_router.get(
    "/{appointment_id}",
    response_model=AppointmentClinicalConditionBlockResponse | None,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_clinical_condition_by_appointment_id_route(
    request: Request, appointment_id: int
):
    if not request.user.doctor:
        raise DoctorNotAssignedException
    doctor_id: int = request.user.doctor.id
    return await hsn_query_block_clinical_condition_by_appointment_id(
        doctor_id, appointment_id
    )
