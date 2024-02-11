
from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, text, DateTime
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class ContragentDBModel(BaseDBModel):
    __tablename__ = 'contragents'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    phone_number = Column(BigInteger, unique=True, nullable=False)
    snils = Column(String(16), unique=True, nullable=False)

    address = Column(Text, nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    patient = relationship("shared.db.models.PatientDBModel", back_populates="contragent", uselist=False)

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
