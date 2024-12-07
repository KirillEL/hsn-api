from typing import Optional

from fastapi import Request

from domains.core.hsn.appointment.blocks.diagnose import (
    HsnCommandBlockDiagnoseUpdateContext,
    hsn_command_block_diagnose_update,
)
from domains.core.hsn.appointment.blocks.diagnose.model import (
    ClassificationFuncClassesType,
    ClassificationAdjacentReleaseType,
    ClassificationNcStageType,
    AppointmentBlockDiagnoseResponse,
)
from .router import block_diagnose_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from pydantic import BaseModel, Field


class UpdateBlockDiagnoseRequestBody(BaseModel):
    diagnose: Optional[str] = Field(None, max_length=1000)
    classification_func_classes: Optional[ClassificationFuncClassesType] = Field(
        ClassificationFuncClassesType.FIRST.value
    )
    classification_adjacent_release: Optional[ClassificationAdjacentReleaseType] = (
        Field(ClassificationAdjacentReleaseType.LOW.value)
    )
    classification_nc_stage: Optional[ClassificationNcStageType] = Field(
        ClassificationNcStageType.I.value
    )

    cardiomyopathy: Optional[bool] = Field(False)
    cardiomyopathy_note: Optional[str] = Field(None, max_length=1000)
    ibc_pikc: Optional[bool] = Field(False)
    ibc_pikc_note: Optional[str] = Field(None, max_length=1000)

    ibc_stenocardia_napr: Optional[bool] = Field(False)
    ibc_stenocardia_napr_note: Optional[str] = Field(None, max_length=1000)
    ibc_another: Optional[bool] = Field(False)
    ibc_another_note: Optional[str] = Field(None, max_length=1000)
    fp_tp: Optional[bool] = Field(False)
    fp_tp_note: Optional[str] = Field(None, max_length=1000)
    ad: Optional[bool] = Field(False)
    ad_note: Optional[str] = Field(None, max_length=1000)
    hobl_ba: Optional[bool] = Field(False)
    hobl_ba_note: Optional[str] = Field(None, max_length=1000)
    onmk_tia: Optional[bool] = Field(False)
    onmk_tia_note: Optional[str] = Field(None, max_length=1000)
    hbp: Optional[bool] = Field(False)
    hbp_note: Optional[str] = Field(None, max_length=1000)
    another: Optional[bool] = Field(False)
    another_note: Optional[str] = Field(None, max_length=1000)


@block_diagnose_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentBlockDiagnoseResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_block_diagnose_route(
    request: Request, appointment_id: int, body: UpdateBlockDiagnoseRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandBlockDiagnoseUpdateContext(
        appointment_id=appointment_id, **body.model_dump()
    )
    doctor_id: int = request.user.doctor.id
    return await hsn_command_block_diagnose_update(doctor_id, context)
