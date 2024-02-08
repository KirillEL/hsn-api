from sqlalchemy import Column, ForeignKey, DateTime, Date, BigInteger, text, Boolean, Integer
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class SuppliedDiagnosesDBModel(BaseDBModel):
    __tablename__ = 'supplied_diagnoses'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_appointment_id = Column(BigInteger, ForeignKey('public.patient_appointments.id'), nullable=False)
    #patient_appointment = relationship('PatientAppointmentsDBModel', back_populates='supplied_diagnoses')

    diagnose_id = Column(BigInteger, ForeignKey('public.diagnoses_catalog.id'), nullable=False)
    #diagnose = relationship('DiagnosesCatalogDBModel', back_populates='supplied_diagnoses')

    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    author_id = Column('created_by', Integer, nullable=False)
    created_by = relationship(UserDBModel,
                              primaryjoin=author_id == foreign(UserDBModel.id),
                              uselist=False,
                              lazy='selectin')

    editor_id = Column('updated_by', Integer)
    updated_by = relationship(UserDBModel,
                              primaryjoin=editor_id == foreign(UserDBModel.id),
                              uselist=False,
                              lazy='selectin')

    deleter_id = Column('deleted_by', Integer)
    deleted_by = relationship(UserDBModel,
                              primaryjoin=deleter_id == foreign(UserDBModel.id),
                              uselist=False,
                              lazy='selectin')
