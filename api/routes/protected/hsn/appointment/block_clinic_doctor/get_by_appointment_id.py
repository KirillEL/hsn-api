from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.clinic_doctor import (
    hsn_get_block_clinic_doctor_by_appointment_id,
)
from domains.core.hsn.appointment.blocks.clinic_doctor.model import (
    AppointmentClinicDoctorBlockResponse,
)
from .router import block_clinic_doctor_router
from fastapi import Request


@block_clinic_doctor_router.get(
    "/{appointment_id}",
    response_model=AppointmentClinicDoctorBlockResponse | None,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_block_clinic_doctor_by_appointment_id_route(
    request: Request, appointment_id: int
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    doctor_id: int = request.user.doctor.id
    return await hsn_get_block_clinic_doctor_by_appointment_id(
        doctor_id, appointment_id
    )
