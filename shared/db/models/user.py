from sqlalchemy import Column, BigInteger, String, Boolean, Enum, text
from .BASE import BaseDBModel
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import relationship


class RoleEnum(Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'


class UserDBModel(BaseDBModel):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    is_active = Column(Boolean, server_default=text("true"))

    role = Column(PGEnum(RoleEnum, name='role'), nullable=False, server_default=text("'DOCTOR'"))

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    doctor = relationship("DoctorDBModel", back_populates="user", uselist=False)
