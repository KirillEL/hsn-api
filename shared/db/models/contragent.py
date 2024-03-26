from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, text, DateTime, Date
from sqlalchemy.orm import relationship, foreign

from .BASE import BaseDBModel
from . import UserDBModel


class ContragentDBModel(BaseDBModel):

    __tablename__ = 'contragents'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    phone_number = Column(Text, unique=True, nullable=False)
    snils = Column(Text, unique=True)
    address = Column(Text, nullable=False)
    mis_number = Column(Text)
    location = Column(Text, nullable=False) # НСО НОВОСИБИРСК ДРУГОЕ
    district = Column(Text) # Район
    date_birth = Column(Text, nullable=False)

    relative_phone_number = Column(Text)
    parent = Column(Text)
    date_dead = Column(Text)

    patient = relationship("PatientDBModel", back_populates="contragent", uselist=False)


