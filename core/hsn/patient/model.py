from typing_extensions import TypedDict
from pydantic import BaseModel, ConfigDict, model_validator, field_validator
from datetime import datetime
from typing import List, Optional
from datetime import date as tdate
import re
from api.exceptions import ValidationException
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
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: bool
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[str] = None
    patient_note: Optional[str] = None

    @field_validator("birth_date", "dod")
    def date_format_validation(cls, v):
        if v is not None:
            try:
                parsed_date = datetime.strptime(v, "%d.%m.%Y")
            except ValueError:
                raise ValidationException(message="Дата должна быть в формате ДД.ММ.ГГГГ")
            if cls.__fields__.get('last_hospitalization_date') and parsed_date > datetime.now():
                raise ValidationException(message="Дата последней госпитализации не должна быть позже чем текущая дата")
        return v

    @field_validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValidationException(message="Номер телефона не валидный!")
        return v

    @model_validator(mode="after")
    def validate_birth_date(self):
        birth_date = datetime.strptime(self.birth_date, "%d.%m.%Y")
        current_date = datetime.now()
        age = (current_date - birth_date).days / 365.25
        if age < 0:
            raise ValidationException(message="Дата рождения не должна быть в будущем.")
        if age > 100:
            raise ValidationException(message="Возраст не должен превышать 100 лет.")
        return self


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
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra='ignore')

    id: int
    user_id: int
    table_columns: list[TableColumns]


class PatientTableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')
    id: int
    table_columns: list[TableColumns]


class DictPatientResponse(TypedDict):
    data: List[PatientResponse | PatientResponseWithoutFullName]
    total: int
