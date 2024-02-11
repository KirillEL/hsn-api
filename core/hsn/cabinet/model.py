from datetime import datetime
from typing import Optional
from core.user.model import UserAuthor
from pydantic import BaseModel, ConfigDict


class Cabinet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    med_id: Optional[int] = None # TODO: поговорить насчет Optional или нет

    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class CabinetFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    med_id: int
    is_deleted: bool
