from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from core.user import UserAuthor


class SuppliedDiagnoses(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_appointment_id: int
    diagnosis_id: int
    date_start: datetime
    date_end: datetime

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None