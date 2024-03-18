from sqlalchemy import Column, ForeignKey, DateTime, Date, Text, BigInteger, text, Boolean, Integer
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class SuppliedDiagnosesDBModel(BaseDBModel):
    __tablename__ = 'supplied_diagnoses'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    patient_appointment_id = Column(BigInteger, ForeignKey('public.patient_appointments.id'), nullable=False)
    diagnose_catalog_id = Column(BigInteger, ForeignKey('public.diagnoses_catalog.id'), nullable=False)
    medicine_prescription_id = Column(BigInteger, ForeignKey('public.medicines_prescription.id'), nullable=False)

    note = Column(Text)

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
