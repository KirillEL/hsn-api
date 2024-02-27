from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from core.user import UserAuthor


class Doctor(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None

    user_id: int
    is_glav: bool

    cabinet_id: Optional[int] = None

    is_deleted: Optional[bool] = False
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class Role(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class UserAndDoctor(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    is_deleted: Optional[bool] = False
    roles: list[Role]
    doctor: Doctor | None
