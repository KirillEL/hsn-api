from .router import block_ekg_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock, hsn_appointment_block_ekg_create, HsnAppointmentBlockEkgCreateContext
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as tdate, datetime
from fastapi import Request

class CreateBlockEkgRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    date_ekg: tdate = Field(default=datetime.today())
    sinus_ritm: bool = Field(False)
    av_blokada: bool = Field(False)
    hypertrofia_lg: bool = Field(False)
    ritm_eks: bool = Field(False)
    av_uzlovaya_tahikardia: bool = Field(False)
    superventrikulyrnaya_tahikardia: bool = Field(False)
    zheludochnaya_tahikardia: bool = Field(False)
    fabrilycia_predcerdiy: bool = Field(False)
    trepetanie_predcerdiy: bool = Field(False)
    another_changes: Optional[str] = Field(None, max_length=1000)

    date_echo_ekg: tdate = Field(default=tdate.today())
    fv: int = Field(None, gt=0)
    sdla: int = Field(None, gt=0)
    lp: int = Field(None, gt=0)
    pp: int = Field(None, gt=0)
    kdr_lg: int = Field(None, gt=0)
    ksr_lg: int = Field(None, gt=0)
    kdo_lg: int = Field(None, gt=0)
    mgp: int = Field(None, gt=0)
    zslg: int = Field(None, gt=0)
    local_hypokines: bool = Field(False)
    distol_disfunction: bool = Field(False)
    anevrizma: bool = Field(False)
    note: Optional[str] = Field(None, max_length=1000)

@block_ekg_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_ekg(request: Request, body: CreateBlockEkgRequestBody):
    context = HsnAppointmentBlockEkgCreateContext(**body.model_dump())
    return await hsn_appointment_block_ekg_create(context)