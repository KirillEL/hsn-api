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


class PatientAppointmentHistoryDto(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')

    id: int
    date: str


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

    def to_dict(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "full_name": self.full_name,
            "age": self.age,
            "birth_date": self.birth_date,
            "dod": self.dod,
            "location": self.location,
            "district": self.district,
            "address": self.address,
            "phone": self.phone,
            "clinic": self.clinic,
            "referring_doctor": self.referring_doctor,
            "referring_clinic_organization": self.referring_clinic_organization,
            "disability": self.disability,
            "lgota_drugs": self.lgota_drugs,
            "has_hospitalization": self.has_hospitalization,
            "count_hospitalization": self.count_hospitalization,
            "last_hospitalization_date": self.last_hospitalization_date,
            "patient_note": self.patient_note,
        }


class PatientWithoutFullNameResponse(BasePatientResponse):
    name: str
    last_name: str
    patronymic: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "patronymic": self.patronymic,
            "gender": self.gender,
            "age": self.age,
            "birth_date": self.birth_date,
            "dod": self.dod,
            "location": self.location,
            "district": self.district,
            "address": self.address,
            "phone": self.phone,
            "clinic": self.clinic,
            "referring_doctor": self.referring_doctor,
            "referring_clinic_organization": self.referring_clinic_organization,
            "disability": self.disability,
            "lgota_drugs": self.lgota_drugs,
            "has_hospitalization": self.has_hospitalization,
            "count_hospitalization": self.count_hospitalization,
            "last_hospitalization_date": self.last_hospitalization_date,
            "patient_note": self.patient_note,
        }


class PatientWithAppointmentHistoryResponse(PatientWithoutFullNameResponse):
    appointment_histories: Optional[list[PatientAppointmentHistoryDto]] = []



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
    data: List[PatientResponse | PatientWithoutFullNameResponse]
    total: int



class PatientAppointmentHistoryResponse(PatientAppointmentHistoryDto):
    pass