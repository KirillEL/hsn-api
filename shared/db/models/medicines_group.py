from sqlalchemy import Column, BigInteger, String, Boolean, text, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class MedicinesGroupDBModel(BaseDBModel):
    __tablename__ = 'medicines_group'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    note = Column(Text, nullable=True)

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
