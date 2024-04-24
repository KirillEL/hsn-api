from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from datetime import date as tdate
from core.hsn.cabinet import Cabinet
from core.hsn.cabinet.model import CabinetFlat
from core.user import UserAuthor
from datetime import date


class Contragent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone_number: str | int  # int
    snils: str
    address: str
    mis_number: str | int  # int
    date_birth: str  # date
    relative_phone_number: Optional[str | int] = None  # int
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
    birth_date: str
    dod: Optional[str] = None
    location: str
    district: str
    address: str
    phone: int
    clinic: str
    patient_note: Optional[str] = None
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: bool
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[str] = None

    contragent: Contragent
    cabinet: Optional[CabinetFlat] = None

    is_deleted: bool

    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class PatientFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    age: int
    gender: str
    birth_date: str
    dod: Optional[str] = None
    location: str
    district: str
    address: str
    phone: int
    clinic: str
    patient_note: Optional[str] = None
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: bool
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[str] = None

    contragent: Contragent
    cabinet: Optional[CabinetFlat] = None


class BasePatientResponse(BaseModel):
    id: int
    gender: str
    age: int
    birth_date: str
    dod: Optional[str] = None
    location: str
    district: str
    address: str
    phone: str
    clinic: str
    patient_note: Optional[str] = None
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: bool
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[str] = None


class PatientResponse(BasePatientResponse):
    full_name: str


class PatientResponseWithoutFullName(BasePatientResponse):
    name: str
    last_name: str
    patronymic: Optional[str] = None


class PatientAvailableColumnsResponse(BaseModel):
    title: str
    value: str
    disabled: Optional[bool] = None