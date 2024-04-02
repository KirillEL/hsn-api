from datetime import datetime, date

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date as tdate

from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from core.user import UserAuthor


class Appointment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    doctor_id: int
    patient_id: int
    date: tdate
    date_next: Optional[tdate] = None

    block_clinic_doctor: AppointmentClinicDoctorBlock
    block_diagnose: AppointmentDiagnoseBlock
    block_laboratory_test: AppointmentLaboratoryTestBlock
    block_ekg: AppointmentEkgBlock
    block_complaint: AppointmentComplaintBlock
    block_clinical_condition: AppointmentClinicalConditionBlock


    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class PatientAppointmentFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    doctor_id: int
    patient_id: int
    date: tdate
    date_next: Optional[tdate] = None

    block_clinic_doctor: AppointmentClinicDoctorBlock
    block_diagnose: AppointmentDiagnoseBlock
    block_laboratory_test: AppointmentLaboratoryTestBlock
    block_ekg: AppointmentEkgBlock
    block_complaint: AppointmentComplaintBlock
    block_clinical_condition: AppointmentClinicalConditionBlock
