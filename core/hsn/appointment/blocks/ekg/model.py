from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date as tdate

class AppointmentEkgBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_ekg: str
    sinus_ritm: Optional[bool] = False
    av_blokada: Optional[bool] = False
    hypertrofia_lg: Optional[bool] = False
    ritm_eks: Optional[bool] = False
    av_uzlovaya_tahikardia: Optional[bool] = False
    superventrikulyrnaya_tahikardia: Optional[bool] = False
    zheludochnaya_tahikardia: Optional[bool] = False
    fabrilycia_predcerdiy: Optional[bool] = False
    trepetanie_predcerdiy: Optional[bool] = False
    another_changes: Optional[str] = None
    date_echo_ekg: str
    fv: int
    sdla: Optional[int] = None
    lp: Optional[int] = None
    pp: Optional[int] = None
    kdr_lg: Optional[int] = None
    ksr_lg: Optional[int] = None
    kdo_lg: Optional[int] = None
    mgp: Optional[int] = None
    zslg: Optional[int] = None
    local_hypokines: Optional[bool] = False
    difusal_hypokines: Optional[bool] = False
    distol_disfunction: Optional[bool] = False
    valvular_lesions: Optional[bool] = False
    anevrizma: Optional[bool] = False
    note: Optional[str] = None