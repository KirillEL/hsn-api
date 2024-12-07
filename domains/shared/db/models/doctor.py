from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    ForeignKey,
    Boolean,
    text,
    DateTime,
)
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class DoctorDBModel(BaseDBModel):
    __tablename__ = "doctors"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    patronymic = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)

    user_id = Column(
        Integer, ForeignKey("public.users.id"), nullable=False, unique=True
    )

    user = relationship("UserDBModel", back_populates="doctor", uselist=False)

    cabinet_id = Column(BigInteger, ForeignKey("public.cabinets.id"), nullable=True)

    cabinet = relationship("CabinetDBModel", back_populates="doctors", uselist=False)

    is_glav = Column(Boolean, nullable=False, server_default=text("false"))

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    author_id = Column("created_by", Integer, nullable=False)
    created_by = relationship(
        UserDBModel,
        primaryjoin=author_id == foreign(UserDBModel.id),
        uselist=False,
        viewonly=True,
        lazy="selectin",
    )

    editor_id = Column("updated_by", Integer)
    updated_by = relationship(
        UserDBModel,
        primaryjoin=editor_id == foreign(UserDBModel.id),
        uselist=False,
        viewonly=True,
        lazy="selectin",
    )

    deleter_id = Column("deleted_by", Integer)
    deleted_by = relationship(
        UserDBModel,
        primaryjoin=deleter_id == foreign(UserDBModel.id),
        uselist=False,
        viewonly=True,
        lazy="selectin",
    )
