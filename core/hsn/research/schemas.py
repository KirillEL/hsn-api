from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.user import UserAuthor


class ResearchFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analyses_id: int
    date: datetime
    patient_appointment_id: int
    patient_hospitalization_id: int


class Research(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analyses_id: int
    date: datetime
    patient_appointment_id: int
    patient_hospitalization_id: int

    is_deleted: bool

    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None