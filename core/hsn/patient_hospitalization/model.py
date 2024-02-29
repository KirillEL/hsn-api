from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from core.user import UserAuthor


class PatientHospitalizationFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    date_start: datetime
    date_end: datetime
    anamnes: Optional[str] = None
    is_deleted: bool


class PatientHospitalization(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int

    date_start: datetime
    date_end: datetime

    anamnes: Optional[str] = None

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None
