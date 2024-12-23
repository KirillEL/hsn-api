from domains.core.hsn.appointment.blocks.diagnose.model import (
    ClassificationFuncClassesType,
    ClassificationAdjacentReleaseType,
    ClassificationNcStageType,
)
from .router import block_diagnose_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.diagnose import (
    hsn_command_appointment_block_diagnose_create,
    HsnCommandAppointmentBlockDiagnoseCreateContext,
)
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Request


class CreateBlockDiagnoseRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)

    diagnose: str = Field(max_length=1000)
    classification_func_classes: ClassificationFuncClassesType = Field(
        ClassificationFuncClassesType.FIRST.value
    )
    classification_adjacent_release: ClassificationAdjacentReleaseType = Field(
        ClassificationAdjacentReleaseType.LOW.value
    )
    classification_nc_stage: ClassificationNcStageType = Field(
        ClassificationNcStageType.I.value
    )

    cardiomyopathy: bool = Field(False)
    cardiomyopathy_note: Optional[str] = Field(None, max_length=1000)
    ibc_pikc: bool = Field(False)
    ibc_pikc_note: Optional[str] = Field(None, max_length=1000)

    ibc_stenocardia_napr: bool = Field(False)
    ibc_stenocardia_napr_note: Optional[str] = Field(None, max_length=1000)
    ibc_another: bool = Field(False)
    ibc_another_note: Optional[str] = Field(None, max_length=1000)
    fp_tp: bool = Field(False)
    fp_tp_note: Optional[str] = Field(None, max_length=1000)
    ad: bool = Field(False)
    ad_note: Optional[str] = Field(None, max_length=1000)
    hobl_ba: bool = Field(False)
    hobl_ba_note: Optional[str] = Field(None, max_length=1000)
    onmk_tia: bool = Field(False)
    onmk_tia_note: Optional[str] = Field(None, max_length=1000)
    hbp: bool = Field(False)
    hbp_note: Optional[str] = Field(None, max_length=1000)
    another: bool = Field(False)
    another_note: Optional[str] = Field(None, max_length=1000)


@block_diagnose_router.post(
    "/create", response_model=int, responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_diagnose(request: Request, body: CreateBlockDiagnoseRequestBody):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentBlockDiagnoseCreateContext(**body.model_dump())
    doctor_id: int = request.user.doctor.id
    return await hsn_command_appointment_block_diagnose_create(doctor_id, context)
