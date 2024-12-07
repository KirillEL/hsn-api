from sqlalchemy import Column, BigInteger, String, Boolean, Enum, text, Text
from .BASE import BaseDBModel
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import relationship


class UserDBModel(BaseDBModel):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)

    is_active = Column(Boolean, server_default=text("true"))

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    doctor = relationship("DoctorDBModel", back_populates="user", uselist=False)

    roles = relationship(
        "RoleDBModel", secondary="public.user_roles", back_populates="users"
    )
