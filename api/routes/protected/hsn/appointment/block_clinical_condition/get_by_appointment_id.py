from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock, \
    hsn_query_block_clinical_condition_by_appointment_id
from .router import block_clinical_condition_router
from fastapi import Request


@block_clinical_condition_router.get(
    "/{appointment_id}",
    response_model=AppointmentClinicalConditionBlock,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_clinical_condition_by_appointment_id_route(
        request: Request,
        appointment_id: int
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    return await hsn_query_block_clinical_condition_by_appointment_id(appointment_id)
