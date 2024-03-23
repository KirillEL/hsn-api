from datetime import datetime, date

from pydantic import BaseModel, ConfigDict
from typing import Optional

from core.user import UserAuthor
from shared.db.models import DisabilityType


class PatientAppointment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    doctor_id: int
    cabinet_id: int

    date: datetime
    date_next: datetime

    weight: Optional[float] = None
    height: Optional[float] = None
    fv_lg: int
    main_diagnose: str
    sistol_ad: float
    diastal_ad: float
    hss: int
    mit: Optional[float] = None
    has_fatigue: bool
    has_dyspnea: bool
    has_swelling_legs: bool
    has_weakness: bool
    has_orthopnea: bool
    has_heartbeat: bool = True
    has_myocardial_infarction: bool
    note: str

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class PatientAppointmentFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    doctor_id: int
    cabinet_id: int
    date: date
    date_next: Optional[datetime] = None
    imt: float
    weight: float
    height: float
    disability: DisabilityType = DisabilityType.NO
    school_hsn_date: Optional[datetime] = None
    classification_func_classes: Optional[str] = None
    classification_adjacent_release: Optional[str] = None
    classification_nc_stage: Optional[str] = None

    has_stenocardia_napryzenya: bool
    has_myocardial_infarction: bool
    has_arteria_hypertension: bool
    arteria_hypertension_age: Optional[int] = None
    fv_lg: int
    main_diagnose: str
    sistol_ad: float
    diastal_ad: float
    hss: int
    mit: float

    appointment_complaint_id: int
    appointment_laboratory_test_id: int
    appointment_blood_chemistry_id: int
    general_blood_analyse_id: int
    hormonal_blood_analyse_id: int
    general_urine_analyse_id: int