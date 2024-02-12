from sqlalchemy import Column, ForeignKey, String, BigInteger, Date, Boolean, text, DateTime, Integer
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class SuppliedMedicationsDBModel(BaseDBModel):
    __tablename__ = 'supplied_medications'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_appointment_id = Column(BigInteger, ForeignKey('public.patient_appointments.id'), nullable=False)

    medicine_id = Column(BigInteger, ForeignKey('public.medicines_catalog.id'), nullable=False)

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
