from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class DoctorDBModel(BaseDBModel):
    __tablename__ = 'doctors'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    patronymic = Column(String(100), nullable=False)

    user_id = Column(BigInteger, ForeignKey('public.users.id'), nullable=False, unique=True)
    cabinet_id = Column(BigInteger, ForeignKey('public.cabinets.id'), nullable=False)

    is_glav = Column(Boolean, nullable=False, server_default='f')

    #cabinet = relationship("CabinetDBModel", back_populates="doctor")
    #user = relationship("UserDBModel", back_populates="doctor")
