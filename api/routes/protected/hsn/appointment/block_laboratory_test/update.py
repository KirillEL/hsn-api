from datetime import datetime
from typing import Optional

from fastapi import Request
from pydantic import BaseModel, Field

from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock, \
    HsnBlockLaboratoryTestUpdateContext, hsn_block_laboratory_test_update
from .router import block_laboratory_test_router
from api.exceptions import ExceptionResponseSchema


class UpdateBlockLaboratoryTestRequestBody(BaseModel):
    nt_pro_bnp: Optional[float] = Field(None, gt=0)
    nt_pro_bnp_date: Optional[str] = Field(None)
    hbalc: Optional[float] = Field(None, gt=0)
    hbalc_date: Optional[str] = Field(None)
    eritrocit: Optional[float] = Field(None, gt=0)
    eritrocit_date: Optional[str] = Field(None)
    hemoglobin: Optional[float] = Field(None, gt=0)
    hemoglobin_date: Optional[str] = Field(None)
    tg: Optional[float] = Field(None, gt=0)
    tg_date: Optional[str] = Field(None)
    lpvp: Optional[float] = Field(None, gt=0)
    lpvp_date: Optional[str] = Field(None)
    lpnp: Optional[float] = Field(None, gt=0)
    lpnp_date: Optional[str] = Field(None)
    general_hc: Optional[float] = Field(None, gt=0)
    general_hc_date: Optional[str] = Field(None)
    natriy: Optional[float] = Field(None, gt=0)
    natriy_date: Optional[str] = Field(None)
    kaliy: Optional[float] = Field(None, gt=0)
    kaliy_date: Optional[str] = Field(None)
    glukoza: Optional[float] = Field(None, gt=0)
    glukoza_date: Optional[str] = Field(None)
    mochevaya_kislota: Optional[float] = Field(None, gt=0)
    mochevaya_kislota_date: Optional[str] = Field(None)
    skf: Optional[float] = Field(None, gt=0)
    skf_date: Optional[str] = Field(None)
    kreatinin: Optional[float] = Field(None, gt=0)
    kreatinin_date: Optional[str] = Field(None)
    protein: Optional[float] = Field(None, gt=0)
    protein_date: Optional[str] = Field(None)
    urine_eritrocit: Optional[float] = Field(None, gt=0)
    urine_eritrocit_date: Optional[str] = Field(None)
    urine_leycocit: Optional[float] = Field(None, gt=0)
    urine_leycocit_date: Optional[str] = Field(None)
    microalbumuria: Optional[float] = Field(None, gt=0)
    microalbumuria_date: Optional[str] = Field(None)
    note: Optional[str] = Field(None, max_length=1000)


@block_laboratory_test_router.patch(
    "/update/{appointment_id}",
    response_model=AppointmentLaboratoryTestBlock,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def update_block_laboratory_test(appointment_id: int, body: UpdateBlockLaboratoryTestRequestBody):
    context = HsnBlockLaboratoryTestUpdateContext(
        appointment_id=appointment_id,
        **body.model_dump()
    )
    return await hsn_block_laboratory_test_update(context)
