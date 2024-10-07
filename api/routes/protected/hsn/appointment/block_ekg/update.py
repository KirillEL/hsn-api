from datetime import datetime
from typing import Optional

from fastapi import Request
from pydantic import BaseModel, Field

from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock, HsnCommandBlockEkgUpdateContext, \
    hsn_command_block_ekg_update
from .router import block_ekg_router


class UpdateBlockEkgRequestBody(BaseModel):
    date_ekg: Optional[str] = Field(default=datetime.today().strftime("%d.%m.%Y"))
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

    date_echo_ekg: Optional[str] = Field(default=datetime.today().strftime("%d.%m.%Y"))
    fv: Optional[int] = Field(None, gt=0)
    sdla: Optional[int] = Field(None, gt=0)
    lp: Optional[int] = Field(None, gt=0)
    pp: Optional[int] = Field(None, gt=0)
    kdr_lg: Optional[int] = Field(None, gt=0)
    ksr_lg: Optional[int] = Field(None, gt=0)
    kdo_lg: Optional[int] = Field(None, gt=0)
    mgp: Optional[int] = Field(None, gt=0)
    zslg: Optional[int] = Field(None, gt=0)
    local_hypokines: Optional[bool] = Field(False)
    distol_disfunction: Optional[bool] = Field(False)
    anevrizma: Optional[bool] = Field(False)
    note: Optional[str] = Field(None, max_length=1000)


@block_ekg_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentEkgBlock,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def update_block_ekg_route(
        request: Request,
        appointment_id: int,
        body: UpdateBlockEkgRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandBlockEkgUpdateContext(
        appointment_id=appointment_id,
        **body.model_dump()
    )
    return await hsn_command_block_ekg_update(context)
