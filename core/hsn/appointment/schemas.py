from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

from core.hsn import Base
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from core.hsn.appointment.blocks.purpose import AppointmentPurposeFlat
from core.user import UserAuthor


class Appointment(Base):
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


class PatientFlatForAppointmentList(Base):
    name: str
    last_name: str
    patronymic: Optional[str] = None


class PatientAppointmentFlat(Base):
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
