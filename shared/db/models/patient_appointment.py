from sqlalchemy import Column, BigInteger, String, DateTime, Float, ForeignKey, Text,text, Integer, Boolean
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from . import UserDBModel
from .BASE import BaseDBModel

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
    has_myocardial_infraction = Column(Boolean, nullable=False, server_default=text("false"))
    has_arteria_hypertension = Column(Boolean, nullable=False, server_default=text("false"))
    arteria_hypertension_age = Column(Integer)

    fv_lg = Column(Integer, nullable=False)
    main_diagnose = Column(Text, nullable=False)
    sistol_ad = Column(Float, nullable=False)
    diastal_ad = Column(Float, nullable=False)
    hss = Column(Integer, nullable=False)
    mit = Column(Float)
    has_fatigue = Column(Boolean, nullable=False, server_default=text("false"))
    has_dyspnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_swelling_legs = Column(Boolean, nullable=False, server_default=text("false"))
    has_weakness = Column(Boolean, nullable=False, server_default=text("false"))
    has_orthopnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_heartbeat = Column(Boolean, nullable=False, server_default=text("true"))
    note_сomplaints = Column(Text)
    note_clinical = Column(Text)
    note_ekg = Column(Text)

    date_ekg = Column(DateTime)
    date_echo_ekg = Column(DateTime)
    fraction_out = Column(Float, nullable=False)
    sdla = Column(Float, nullable=False)

    nt_pro_bnp = Column(Float, nullable=False)
    date_nt_pro_bnp = Column(DateTime)
    microalbumuria = Column(Float, nullable=False)
    date_microalbumuria = Column(DateTime)


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


