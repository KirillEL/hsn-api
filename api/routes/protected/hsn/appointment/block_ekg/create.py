from .router import block_ekg_router
from api.exceptions import ExceptionResponseSchema, ValidationException, DoctorNotAssignedException
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock, hsn_command_appointment_block_ekg_create, \
    HsnCommandAppointmentBlockEkgCreateContext
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date as tdate, datetime
from fastapi import Request


class CreateBlockEkgRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    date_ekg: str = Field(default=None)
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

    date_echo_ekg: str = Field(default=None)
    fv: float = Field(None, gt=0)
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
    local_hypokines: bool = Field(False)
    difusal_hypokines: bool = Field(False)
    distol_disfunction: bool = Field(False)
    valvular_lesions: bool = Field(False)
    anevrizma: bool = Field(False)
    note: Optional[str] = Field(None, max_length=1000)

    @field_validator('date_ekg', 'date_echo_ekg')
    def check_date_format(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")


@block_ekg_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_ekg_route(request: Request, body: CreateBlockEkgRequestBody):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentBlockEkgCreateContext(**body.model_dump())
    doctor_id: int = request.user.doctor.id
    return await hsn_command_appointment_block_ekg_create(doctor_id, context)
