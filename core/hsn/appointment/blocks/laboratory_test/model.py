from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date as tdate

class AppointmentLaboratoryTestBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    # ГОРМОНАЛЬНЫЙ АНАЛИЗ КРОВИ
    nt_pro_bnp: Optional[float] = None
    nt_pro_bnp_date: Optional[str] = None
    hbalc: Optional[float] = None
    hbalc_date: Optional[str] = None

    # ОБЩИЙ АНАЛИЗ КРОВИ
    eritrocit: Optional[float] = None
    eritrocit_date: Optional[str] = None
    hemoglobin: Optional[float] = None
    hemoglobin_date: Optional[str] = None

    # БИОХИМ АНАЛИЗ КРОВИ
    tg: Optional[float] = None
    tg_date: Optional[str] = None
    lpvp: Optional[float] = None
    lpvp_date: Optional[str] = None
    lpnp: Optional[float] = None
    lpnp_date: Optional[str] = None
    general_hc: Optional[float] = None
    general_hc_date: Optional[str] = None
    natriy: Optional[float] = None
    natriy_date: Optional[str] = None
    kaliy: Optional[float] = None
    kaliy_date: Optional[str] = None
    glukoza: Optional[float] = None
    glukoza_date: Optional[str] = None
    mochevaya_kislota: Optional[float] = None
    mochevaya_kislota_date: Optional[str] = None
    skf: Optional[float] = None
    skf_date: Optional[str] = None
    kreatinin: Optional[float] = None
    kreatinin_date: Optional[str] = None

    # ОБЩИЙ АНАЛИЗ МОЧИ
    protein: Optional[float] = None
    protein_date: Optional[str] = None
    urine_eritrocit: Optional[float] = None
    urine_eritrocit_date: Optional[str] = None
    urine_leycocit: Optional[float] = None
    urine_leycocit_date: Optional[str] = None
    microalbumuria: Optional[float] = None
    microalbumuria_date: Optional[str] = None
    note: Optional[str] = None