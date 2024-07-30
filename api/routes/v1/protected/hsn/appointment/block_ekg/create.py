from .router import block_ekg_router
from api.exceptions import ExceptionResponseSchema, ValidationException
from core.hsn.appointment.blocks.ekg import (
    AppointmentEkgBlock,
    hsn_appointment_block_ekg_create,
    HsnAppointmentBlockEkgCreateContext,
)
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date as tdate, datetime
from fastapi import Request


class CreateBlockEkgRequest(BaseModel):
    appointment_id: int = Field(gt=0)
    date_ekg: str = Field(default=datetime.today().strftime("%d.%m.%Y"))
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

    date_echo_ekg: str = Field(default=datetime.today().strftime("%d.%m.%Y"))
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

    @field_validator("date_ekg", "date_echo_ekg")
    def check_date_format(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")


@block_ekg_router.post(
    "/create", response_model=int, responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_ekg(request: Request, body: CreateBlockEkgRequest):
    context = HsnAppointmentBlockEkgCreateContext(**body.model_dump())
    return await hsn_appointment_block_ekg_create(context)
