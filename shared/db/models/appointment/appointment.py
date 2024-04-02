from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, text
from sqlalchemy.orm import relationship, foreign

from .. import UserDBModel
from ..BASE import BaseDBModel
from .blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from .blocks.block_diagnose import AppointmentDiagnoseBlockDBModel
from .blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from .blocks.block_ekg import AppointmentEkgBlockDBModel
from .blocks.block_complaint import AppointmentComplaintBlockDBModel
from .blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
class AppointmentDBModel(BaseDBModel):
    __tablename__ = 'appointments'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    doctor_id = Column(Integer, ForeignKey('public.doctors.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('public.patients.id'), nullable=False)
    date = Column(DateTime(timezone=False), nullable=False, server_default=text("now()"))
    date_next = Column(DateTime(timezone=False))

    block_clinic_doctor_id = Column(Integer, ForeignKey('public.appointment_block_clinic_doctors.id'), nullable=False)
    block_clinic_doctor = relationship(AppointmentBlockClinicDoctorDBModel, uselist=False)

    block_diagnose_id = Column(Integer, ForeignKey('public.appointment_block_diagnoses.id'), nullable=False)
    block_diagnose = relationship(AppointmentDiagnoseBlockDBModel, uselist=False)

    block_laboratory_test_id = Column(Integer, ForeignKey('public.appointment_block_laboratory_tests.id'), nullable=False)
    block_laboratory_test = relationship(AppointmentLaboratoryTestBlockDBModel, uselist=False)

    block_ekg_id = Column(Integer, ForeignKey('public.appointment_block_ekgs.id'), nullable=False)
    block_ekg = relationship(AppointmentEkgBlockDBModel, uselist=False)

    block_complaint_id = Column(Integer, ForeignKey('public.appointment_block_complaints.id'), nullable=False)
    block_complaint = relationship(AppointmentComplaintBlockDBModel, uselist=False)

    block_clinical_condition_id = Column(Integer, ForeignKey('public.appointment_block_clinical_conditions.id'), nullable=False)
    block_clinical_condition = relationship(AppointmentClinicalConditionBlockDBModel, uselist=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    author_id = Column('created_by', Integer, nullable=False)
    created_by = relationship(UserDBModel,
                              primaryjoin=author_id == foreign(UserDBModel.id),
                              uselist=False,
                              viewonly=True,
                              lazy='selectin')

    editor_id = Column('updated_by', Integer)
    updated_by = relationship(UserDBModel,
                              primaryjoin=editor_id == foreign(UserDBModel.id),
                              uselist=False,
                              viewonly=True,
                              lazy='selectin')

    deleter_id = Column('deleted_by', Integer)
    deleted_by = relationship(UserDBModel,
                              primaryjoin=deleter_id == foreign(UserDBModel.id),
                              uselist=False,
                              viewonly=True,
                              lazy='selectin')