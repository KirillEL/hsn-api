from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from core.user import UserAuthor
from datetime import date


class Contragent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone_number: int
    snils: str
    address: str
    mis_number: int
    date_birth: date
    relative_phone_number: int
    parent: Optional[str] = None
    date_dead: Optional[date] = None


class Patient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    age: int
    gender: str
    height: int
    main_diagnose: Optional[str] = None
    disability: str
    date_setup_diagnose: Optional[datetime] = None
    school_hsn_date: Optional[datetime] = None
    have_hospitalization: bool
    count_hospitalizations: int
    lgota_drugs: str
    last_hospitalization_id: Optional[int] = None
    note: str
    has_chronic_heart: bool
    classification_func_classes: str
    has_stenocardia: bool
    has_arteria_hypertension: bool
    arteria_hypertension_age: int

    contragent: Contragent

    is_deleted: bool

    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None
