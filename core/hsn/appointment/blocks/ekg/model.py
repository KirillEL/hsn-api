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
    fv: float
    sdla: Optional[float] = None
    lp: Optional[float] = None
    lp2: Optional[float] = None
    pp: Optional[float] = None
    pp2: Optional[float] = None
    kdr_lg: Optional[float] = None
    ksr_lg: Optional[float] = None
    kdo_lg: Optional[float] = None
    kso_lg: Optional[float] = None
    mgp: Optional[float] = None
    zslg: Optional[float] = None
    local_hypokines: Optional[bool] = False
    difusal_hypokines: Optional[bool] = False
    distol_disfunction: Optional[bool] = False
    valvular_lesions: Optional[bool] = False
    anevrizma: Optional[bool] = False
    note: Optional[str] = None


class AppointmentEkgBlockResponse(AppointmentEkgBlock):
    pass