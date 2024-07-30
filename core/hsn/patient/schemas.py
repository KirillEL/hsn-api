from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from datetime import date as tdate

from core.hsn import Base
from core.hsn.cabinet import Cabinet
from core.hsn.cabinet.schemas import CabinetFlat
from core.user import UserAuthor
from datetime import date


class Contragent(Base):
    phone_number: str
    snils: str
    address: str
    mis_number: str | int
    date_birth: str
    date_dead: Optional[str] = None  # date


class Patient(Base):
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


class PatientFlat(Base):
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
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: bool
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[str] = None
    patient_note: Optional[str] = None


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


class TableColumns(BaseModel):
    dataIndex: str
    hidden: bool


class PatientTableColumns(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, extra="ignore"
    )

    id: int
    user_id: int
    table_columns: list[TableColumns]


class PatientTableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    id: int
    table_columns: list[TableColumns]
