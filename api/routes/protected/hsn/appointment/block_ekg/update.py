from typing import Optional

from fastapi import Request
from pydantic import BaseModel, Field

from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from domains.core.hsn.appointment.blocks.ekg import (
    HsnCommandBlockEkgUpdateContext,
    hsn_command_block_ekg_update,
)
from domains.core.hsn.appointment.blocks.ekg.model import AppointmentEkgBlockResponse
from .router import block_ekg_router


class UpdateBlockEkgRequestBody(BaseModel):
    date_ekg: Optional[str] = Field(default=None)
    sinus_ritm: Optional[bool] = Field(False)
    av_blokada: Optional[bool] = Field(False)
    hypertrofia_lg: Optional[bool] = Field(False)
    ritm_eks: Optional[bool] = Field(False)
    av_uzlovaya_tahikardia: Optional[bool] = Field(False)
    superventrikulyrnaya_tahikardia: Optional[bool] = Field(False)
    zheludochnaya_tahikardia: Optional[bool] = Field(False)
    fabrilycia_predcerdiy: Optional[bool] = Field(False)
    trepetanie_predcerdiy: Optional[bool] = Field(False)
    another_changes: Optional[str] = Field(None, max_length=1000)

    date_echo_ekg: Optional[str] = Field(default=None)
    fv: Optional[float] = Field(None, gt=0)
    sdla: Optional[float] = Field(None, gt=0)
    lp: Optional[float] = Field(None, gt=0)
    lp2: Optional[float] = Field(None, gt=0)
    pp: Optional[float] = Field(None, gt=0)
    pp2: Optional[float] = Field(None, gt=0)
    kdr_lg: Optional[float] = Field(None, gt=0)
    ksr_lg: Optional[float] = Field(None, gt=0)
    kdo_lg: Optional[float] = Field(None, gt=0)
    kso_lg: Optional[float] = Field(None, gt=0)
    mgp: Optional[float] = Field(None, gt=0)
    zslg: Optional[float] = Field(None, gt=0)
    local_hypokines: Optional[bool] = Field(False)
    difusal_hypokines: Optional[bool] = Field(False)
    distol_disfunction: Optional[bool] = Field(False)
    valvular_lesions: Optional[bool] = Field(False)
    anevrizma: Optional[bool] = Field(False)
    note: Optional[str] = Field(None, max_length=1000)


@block_ekg_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentEkgBlockResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def update_block_ekg_route(
    request: Request, appointment_id: int, body: UpdateBlockEkgRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandBlockEkgUpdateContext(
        appointment_id=appointment_id, **body.model_dump()
    )
    doctor_id: int = request.user.doctor.id
    return await hsn_command_block_ekg_update(doctor_id, context)
