from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from core.user import UserAuthor


class MedicinePrescription(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    medicine_group_id: int
    patient_appointment_id: int

    name: str
    mnn: Optional[str] = None
    dosa: int

    note: Optional[str] = None

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None
