import datetime

from .router import block_laboratory_test_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock, hsn_appointment_block_laboratory_test_create, HsnAppointmentBlockLaboratoryTestCreateContext
from pydantic import BaseModel, Field
from datetime import date as tdate
from typing import Optional
from fastapi import Request

class CreateBlockLaboratoryTestRequestBody(BaseModel):
    nt_pro_bnp: float = Field(gt=0)
    nt_pro_bnp_date: tdate = Field(default=datetime.date.today())
    hbalc: float = Field(gt=0)
    hbalc_date: tdate = Field(default=datetime.date.today())
    eritrocit: float = Field(gt=0)
    eritrocit_date: tdate = Field(default=datetime.date.today())
    hemoglobin: float = Field(gt=0)
    hemoglobin_date: tdate = Field(default=datetime.date.today())
    tg: float = Field(gt=0)
    tg_date: tdate = Field(default=datetime.date.today())
    lpvp: float = Field(gt=0)
    lpvp_date: tdate = Field(default=datetime.date.today())
    lpnp: float = Field(gt=0)
    lpnp_date: tdate = Field(default=datetime.date.today())
    general_hc: float = Field(gt=0)
    general_hc_date: tdate = Field(default=datetime.date.today())
    natriy: float = Field(gt=0)
    natriy_date: tdate = Field(default=datetime.date.today())
    kaliy: float = Field(gt=0)
    kaliy_date: tdate = Field(default=datetime.date.today())
    glukoza: float = Field(gt=0)
    glukoza_date: tdate = Field(default=datetime.date.today())
    mochevaya_kislota: float = Field(gt=0)
    mochevaya_kislota_date: tdate = Field(default=datetime.date.today())
    skf: float = Field(gt=0)
    skf_date: tdate = Field(default=datetime.date.today())
    kreatinin: float = Field(gt=0)
    kreatinin_date: tdate = Field(default=datetime.date.today())
    protein: float = Field(gt=0)
    protein_date: tdate = Field(default=datetime.date.today())
    urine_eritrocit: float = Field(gt=0)
    urine_eritrocit_date: tdate = Field(default=datetime.date.today())
    urine_leycocit: float = Field(gt=0)
    urine_leycocit_date: tdate = Field(default=datetime.date.today())
    microalbumuria: float = Field(gt=0)
    microalbumuria_date: tdate = Field(default=datetime.date.today())
    note: Optional[str] = Field(None, max_length=1000)


@block_laboratory_test_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_laboratory_test(request: Request, body: CreateBlockLaboratoryTestRequestBody):
    context = HsnAppointmentBlockLaboratoryTestCreateContext(**body.model_dump())
    return await hsn_appointment_block_laboratory_test_create(context)