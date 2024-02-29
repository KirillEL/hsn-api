from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

from core.user import UserAuthor


class MedicinesGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    note: Optional[str] = None

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None

