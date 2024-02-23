from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, text, DateTime, Date
from sqlalchemy.orm import relationship, foreign

from .BASE import BaseDBModel
from . import UserDBModel


class ContragentDBModel(BaseDBModel):

    __tablename__ = 'contragents'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    phone_number = Column(Text, unique=True, nullable=False)
    snils = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    mis_number = Column(Text, nullable=False)
    date_birth = Column(Text, nullable=False)
    relative_phone_number = Column(Text, nullable=False)
    parent = Column(Text)
    date_dead = Column(Text)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    patient = relationship("PatientDBModel", back_populates="contragent", uselist=False)

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
