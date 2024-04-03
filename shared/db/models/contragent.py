from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, text, DateTime, Date
from sqlalchemy.orm import relationship, foreign

from .BASE import BaseDBModel
from . import UserDBModel


class ContragentDBModel(BaseDBModel):

    __tablename__ = 'contragents'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    patronymic = Column(String(255))
    birth_date = Column(String(255), nullable=False)
    dod = Column(String(255))

    patient = relationship("PatientDBModel", back_populates="contragent", uselist=False)


