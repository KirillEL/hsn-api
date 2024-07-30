from typing import Optional

from core.hsn.appointment.blocks.clinic_doctor import (
    AppointmentClinicDoctorBlock,
    HsnBlockClinicDoctorUpdateContext,
    hsn_block_clinic_doctor_update,
)
from core.hsn.appointment.blocks.clinic_doctor.model import (
    DisabilityType,
    LgotaDrugsType,
)
from core.hsn.appointment.blocks.clinical_condition import (
    HsnBlockClinicalConditionUpdateContext,
)
from .router import block_clinic_doctor_router
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field


class UpdateBlockClinicDoctorRequestBody(BaseModel):
    referring_doctor: Optional[str] = Field(None, max_length=500)
    referring_clinic_organization: Optional[str] = Field(None, max_length=500)
    disability: Optional[DisabilityType] = Field(DisabilityType.NO.value)
    lgota_drugs: Optional[LgotaDrugsType] = Field(LgotaDrugsType.NO.value)
    has_hospitalization: Optional[bool] = Field(False)
    count_hospitalization: Optional[int] = Field(None, gt=0)
    last_hospitalization_date: Optional[str] = Field(None)


@block_clinic_doctor_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentClinicDoctorBlock,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_block_clinic_doctor(
    appointment_id: int, body: UpdateBlockClinicDoctorRequestBody
):
    context = HsnBlockClinicDoctorUpdateContext(
        appointment_id=appointment_id, **body.model_dump()
    )
    return await hsn_block_clinic_doctor_update(context)
