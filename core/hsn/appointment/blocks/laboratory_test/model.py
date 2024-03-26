from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date as tdate

class AppointmentLaboratoryTestBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    # ГОРМОНАЛЬНЫЙ АНАЛИЗ КРОВИ
    nt_pro_bnp: Optional[float] = None
    nt_pro_bnp_date: Optional[tdate] = None
    hbalc: Optional[float] = None
    hbalc_date: Optional[tdate] = None

    # ОБЩИЙ АНАЛИЗ КРОВИ
    eritrocit: Optional[float] = None
    eritrocit_date: Optional[tdate] = None
    hemoglobin: Optional[float] = None
    hemoglobin_date: Optional[tdate] = None

    # БИОХИМ АНАЛИЗ КРОВИ
    tg: Optional[float] = None
    tg_date: Optional[tdate] = None
    lpvp: Optional[float] = None
    lpvp_date: Optional[tdate] = None
    lpnp: Optional[float] = None
    lpnp_date: Optional[tdate] = None
    general_hc: Optional[float] = None
    general_hc_date: Optional[tdate] = None
    natriy: Optional[float] = None
    natriy_date: Optional[tdate] = None
    kaliy: Optional[float] = None
    kaliy_date: Optional[tdate] = None
    glukoza: Optional[float] = None
    glukoza_date: Optional[tdate] = None
    mochevaya_kislota: Optional[float] = None
    mochevaya_kislota_date: Optional[tdate] = None
    skf: Optional[float] = None
    skf_date: Optional[tdate] = None
    kreatinin: Optional[float] = None
    kreatinin_date: Optional[tdate] = None

    # ОБЩИЙ АНАЛИЗ МОЧИ
    protein: Optional[float] = None
    protein_date: Optional[tdate] = None
    urine_eritrocit: Optional[float] = None
    urine_eritrocit_date: Optional[tdate] = None
    urine_leycocit: Optional[float] = None
    urine_leycocit_date: Optional[tdate] = None
    microalbumuria: Optional[float] = None
    microalbumuria_date: Optional[tdate] = None
    note: Optional[str] = None