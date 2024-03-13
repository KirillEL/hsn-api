from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from core.user import UserAuthor
from datetime import date


class Contragent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone_number: str | int # int
    snils: str
    address: str
    mis_number: str | int  # int
    date_birth: str  # date
    relative_phone_number: str | int  # int
    parent: Optional[str] = None
    date_dead: Optional[str] = None  # date




class Patient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    cabinet_id: Optional[int] = None
    age: int
    gender: str
    height: int
    date_setup_diagnose: Optional[datetime] = None
    lgota_drugs: str
    note: Optional[str] = None

    contragent: Contragent

    is_deleted: bool

    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None
