from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.user import UserAuthor


class AppointmentPurpose(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    medicine_prescription_id: int
    note: Optional[str] = None

    is_deleted: bool

    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class AppointmentPurposeFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    medicine_prescription_id: int
    note: Optional[str] = None