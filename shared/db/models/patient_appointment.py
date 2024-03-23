from enum import Enum

from sqlalchemy import Column, BigInteger, String, DateTime, Float, ForeignKey, Text,text, Integer, Boolean
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from . import UserDBModel
from .BASE import BaseDBModel
from shared.db.models.appointment_complaint import AppointmentComplaintDBModel
from shared.db.models.appointment_laboratory_test import AppointmentLaboratoryTestDBModel
from shared.db.models.general_blood_analyse import GeneralBloodAnalyseDBModel
from shared.db.models.general_urine_analyse import GeneralUrineAnalyseDBModel
from shared.db.models.hormonal_blood_analyse import HormonalBloodAnalyseDBModel
from shared.db.models.blood_chemistry import BloodChemistryDBModel

class DisabilityType(Enum):
    NO = 'нет'
    FIRST = 'первая'
    SECOND = 'вторая'
    THIRD = 'третья'


disabilities = ('no', 'first', 'second', 'third')
classifications = ('fk1', 'fk2', 'fk3', 'fk4')
classifications_adjacent_release = ('<40', '40-49', '>50')
classification_nc_stage = ('IA', 'IB', 'IIA', 'IIB', 'IIIA', 'IIIB')
class PatientAppointmentsDBModel(BaseDBModel):
    __tablename__ = 'patient_appointments'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_id = Column(BigInteger, ForeignKey('public.patients.id'), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey('public.doctors.id'), nullable=False)
    cabinet_id = Column(BigInteger, ForeignKey('public.cabinets.id'))
    date = Column(DateTime(timezone=True), nullable=False)
    date_next = Column(DateTime(timezone=True), nullable=True)
    imt = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    disability = Column(PGEnum(*disabilities, name="disability_type", create_type=False), nullable=False, server_default=text("'no'"))
    school_hsn_date = Column(DateTime)
    classification_func_classes = Column(PGEnum(*classifications, name="classification_func_classes_type", create_type=False))
    classification_adjacent_release = Column(PGEnum(*classifications_adjacent_release, name="classification_adjacent_release_type", create_type=False))
    classification_nc_stage = Column(PGEnum(*classification_nc_stage, name="classification_nc_stage_type", create_type=False))
    has_stenocardia_napryzenya = Column(Boolean, nullable=False, server_default=text("false"))
    has_myocardial_infarction = Column(Boolean, nullable=False, server_default=text("false"))
    has_arteria_hypertension = Column(Boolean, nullable=False, server_default=text("false"))
    arteria_hypertension_age = Column(Integer)

    fv_lg = Column(Integer, nullable=False)
    main_diagnose = Column(Text, nullable=False)
    sistol_ad = Column(Float, nullable=False)
    diastal_ad = Column(Float, nullable=False)
    hss = Column(Integer, nullable=False)
    mit = Column(Float)

    appointment_complaint_id = Column(Integer, ForeignKey('public.appointment_complaints.id'), unique=True)
    appointment_complaint = relationship(AppointmentComplaintDBModel, uselist=False)

    appointment_laboratory_test_id = Column(Integer, ForeignKey('public.appointment_laboratory_tests.id'),  unique=True)
    appointment_laboratory_test = relationship(AppointmentLaboratoryTestDBModel, uselist=False)

    appointment_blood_chemistry_id = Column(Integer, ForeignKey('public.blood_chemistries.id'),  unique=True)
    appointment_blood_chemistry = relationship(BloodChemistryDBModel, uselist=False)

    general_blood_analyse_id = Column(Integer, ForeignKey('public.general_blood_analyses.id'),  unique=True)
    general_blood_analyse = relationship(GeneralBloodAnalyseDBModel, uselist=False)

    hormonal_blood_analyse_id = Column(Integer, ForeignKey('public.hormonal_blood_analyses.id'), unique=True)
    hormonal_blood_analyse = relationship(HormonalBloodAnalyseDBModel, uselist=False)

    general_urine_analyse_id = Column(Integer, ForeignKey('public.general_urine_analyses.id'), unique=True)
    general_urine_analyse = relationship(GeneralUrineAnalyseDBModel, uselist=False)

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


