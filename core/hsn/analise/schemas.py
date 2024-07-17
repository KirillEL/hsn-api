from datetime import datetime
from typing import Optional

from core.user import UserAuthor
from pydantic import BaseModel, ConfigDict


class Analise(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    count_index: int
    patient_hospitalization_id: int

    is_deleted: bool

    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None