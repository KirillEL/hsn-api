from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date as tdate


class AppointmentLaboratoryTestBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int

    # ГОРМОНАЛЬНЫЙ АНАЛИЗ КРОВИ
    nt_pro_bnp: Optional[float] = None
    nt_pro_bnp_date: Optional[str] = None
    hbalc: Optional[float] = None
    hbalc_date: Optional[str] = None

    # ОБЩИЙ АНАЛИЗ КРОВИ
    eritrocit: Optional[float] = None
    hemoglobin: Optional[float] = None
    oak_date: Optional[str] = None

    # БИОХИМ АНАЛИЗ КРОВИ
    tg: Optional[float] = None
    lpvp: Optional[float] = None
    lpnp: Optional[float] = None
    general_hc: Optional[float] = None
    natriy: Optional[float] = None
    kaliy: Optional[float] = None
    glukoza: Optional[float] = None
    mochevaya_kislota: Optional[float] = None
    skf: Optional[float] = None
    kreatinin: Optional[float] = None
    bk_date: Optional[str] = None

    # ОБЩИЙ АНАЛИЗ МОЧИ
    protein: Optional[str] = None
    urine_eritrocit: Optional[str] = None
    urine_leycocit: Optional[str] = None
    microalbumuria: Optional[str] = None
    am_date: Optional[str] = None
    note: Optional[str] = None


class AppointmentLaboratoryTestBlockResponse(AppointmentLaboratoryTestBlock):
    pass
