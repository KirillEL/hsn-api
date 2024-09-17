from sqlalchemy import Column, String, BigInteger, ForeignKey, Text, Boolean, text, DateTime, Integer
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel
from .medicines_group import MedicinesGroupDBModel


class MedicinesPrescriptionDBModel(BaseDBModel):
    __tablename__ = 'medicine_prescriptions'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    appointment_purpose_id = Column(BigInteger, ForeignKey('public.appointment_purposes.id'), nullable=False)

    medicine_group_id = Column(Integer, ForeignKey('public.medicines_group.id'), nullable=False)

    medicine_group = relationship(MedicinesGroupDBModel, uselist=False)

    dosa = Column(String(10), nullable=False)
    #name = Column(Text, nullable=False)
    note = Column(String(500), nullable=True)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    author_id = Column('created_by', Integer, nullable=True)
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
