from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from core.hsn.cabinet.schemas import CabinetFlat
from core.user import UserAuthor, User


class DoctorFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    phone_number: int

    user_id: int
    is_glav: bool

    cabinet_id: Optional[int] = None

    is_deleted: Optional[bool] = False


class DoctorWithUserAndCabinetFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    phone_number: int

    user_id: int
    user: User
    is_glav: bool

    cabinet_id: Optional[int] = None
    cabinet: Optional[CabinetFlat] = None


class Doctor(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    phone_number: int

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
    doctor: Optional[DoctorFlat] = None
