from sqlalchemy import Column, String, BigInteger, Date, ForeignKey
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel



class PatientDBModel(BaseDBModel):
    __tablename__ = 'patients'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    patronymic = Column(String(100))
    gender = Column(String(1), nullable=False)

    cabinet_id = Column(BigInteger, ForeignKey('public.cabinets.id'), nullable=False)
    cabinet = relationship('CabinetDBModel', back_populates="patients")

    contragent_id = Column(BigInteger, ForeignKey('public.contragents.id'), nullable=False, unique=True)
    contragent = relationship('ContragentDBModel', back_populates="patients")




