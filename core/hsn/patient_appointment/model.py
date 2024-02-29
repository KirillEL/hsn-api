from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

from core.user import UserAuthor


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
    note: str

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None

