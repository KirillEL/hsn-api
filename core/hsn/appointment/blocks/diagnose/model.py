from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentDiagnoseBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    diagnose: str
    classification_func_classes: str
    classification_nc_stage: str

    cardiomyopathy: Optional[bool] = False
    cardiomyopathy_note: Optional[str] = None

    ibc_pikc: Optional[bool] = False
    ibc_pikc_note: Optional[str] = None

    ibc_stenocardia_napr: Optional[bool] = False
    ibc_stenocardia_napr_note: Optional[str] = None

    ibc_another: Optional[bool] = False
    ibc_another_note: Optional[str] = None

    fp_tp: Optional[bool] = False
    fp_tp_note: Optional[str] = None

    ad: Optional[bool] = False
    ad_note: Optional[str] = None

    cd: Optional[bool] = False
    cd_note: Optional[str] = None

    hobl_ba: Optional[bool] = False
    hobl_ba_note: Optional[str] = None

    onmk_tia: Optional[bool] = False
    onmk_tia_note: Optional[str] = None

    hbp: Optional[bool] = False
    hbp_note: Optional[str] = None

    another: Optional[str] = None