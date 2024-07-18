from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from core.hsn import Base
from core.hsn.cabinet.schemas import CabinetFlat
from core.user import UserAuthor, User


class DoctorFlat(Base):
    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    phone_number: int

    user_id: int
    is_glav: bool

    cabinet_id: Optional[int] = None

    is_deleted: Optional[bool] = False


class DoctorWithUserAndCabinetFlat(Base):
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


class Doctor(Base):
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


class Role(Base):
    name: str


class UserAndDoctor(Base):
    id: int
    login: str
    is_deleted: Optional[bool] = False
    roles: list[Role]
    doctor: Optional[DoctorFlat] = None
