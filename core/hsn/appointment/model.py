from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from core.hsn.appointment.blocks.base_model import (
    AppointmentBlockBooleanTextFieldsResponse,
    AppointmentBlockTextDateLaboratoryTestFieldsResponse,
)
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
)
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from core.hsn.appointment.blocks.complaint.model import (
    AppointmentBlockBooleanFieldsResponse,
    AppointmentBlockEkgBooleanFieldsResponse,
)
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from core.hsn.drug_group.schemas import DrugGroupFieldsResponse, DrugFieldsSchema
from core.user import UserAuthor


class Appointment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    doctor_id: int
    patient_id: int
    date: str
    date_next: Optional[str] = None

    block_clinic_doctor: AppointmentClinicDoctorBlock
    block_diagnose: AppointmentDiagnoseBlock
    block_laboratory_test: AppointmentLaboratoryTestBlock
    block_ekg: AppointmentEkgBlock
    block_complaint: AppointmentComplaintBlock
    block_clinical_condition: AppointmentClinicalConditionBlock

    status: str
    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class AppointmentCreateResponse(Appointment):
    pass


class PatientFlatForAppointmentList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    last_name: str
    patronymic: Optional[str] = None


class PatientAppointmentFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    doctor_id: int
    full_name: str
    date: str
    date_next: Optional[str] = None

    block_clinic_doctor: Optional[AppointmentClinicDoctorBlock] = None
    block_diagnose: Optional[AppointmentDiagnoseBlock] = None
    block_laboratory_test: Optional[AppointmentLaboratoryTestBlock] = None
    block_ekg: Optional[AppointmentEkgBlock] = None
    block_complaint: Optional[AppointmentComplaintBlock] = None
    block_clinical_condition: Optional[AppointmentClinicalConditionBlock] = None
    purposes: Optional[list[AppointmentPurposeFlat]] = None

    status: str


class AppointmentsListDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    doctor_id: int
    full_name: str
    date: str
    date_next: Optional[str] = None
    status: str


class AppointmentListResponse(AppointmentsListDto):
    pass


class AppointmentFlatResponse(PatientAppointmentFlat):
    pass


class PatientInfoDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    birth_date: str
    gender: str
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


class PatientAppointmentByIdDto(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    doctor_id: int
    patient: PatientInfoDto
    date: str
    date_next: Optional[str] = None

    block_clinic_doctor: Optional[AppointmentClinicDoctorBlock] = None
    block_diagnose: Optional[AppointmentDiagnoseBlock] = None
    block_laboratory_test: Optional[AppointmentLaboratoryTestBlock] = None
    block_ekg: Optional[AppointmentEkgBlock] = None
    block_complaint: Optional[AppointmentComplaintBlock] = None
    block_clinical_condition: Optional[AppointmentClinicalConditionBlock] = None
    purposes: Optional[list[AppointmentPurposeFlat]] = None

    status: str


class PatientAppointmentByIdResponse(PatientAppointmentByIdDto):
    pass


class AppointmentFields(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    diagnose: List[AppointmentBlockBooleanTextFieldsResponse]
    complaints: List[AppointmentBlockBooleanFieldsResponse]
    laboratory_test: AppointmentBlockTextDateLaboratoryTestFieldsResponse
    ekg: AppointmentBlockEkgBooleanFieldsResponse
    purpose: List[DrugFieldsSchema]
    clinical_condition: List[AppointmentBlockBooleanFieldsResponse]


class AppointmentFieldsResponse(AppointmentFields):
    pass
