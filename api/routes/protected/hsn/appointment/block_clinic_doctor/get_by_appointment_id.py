from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock, \
    hsn_get_block_clinic_doctor_by_appointment_id
from core.hsn.appointment.blocks.clinical_condition import hsn_get_block_clinical_condition_by_appointment_id
from .router import block_clinic_doctor_router


@block_clinic_doctor_router.get(
    "/{appointment_id}",
    response_model=AppointmentClinicDoctorBlock,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_block_clinic_doctor_by_appointment_id(appointment_id: int):
    return await hsn_get_block_clinic_doctor_by_appointment_id(appointment_id)
