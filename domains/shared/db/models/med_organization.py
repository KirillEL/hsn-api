from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    text,
    DateTime,
    Integer,
    Text,
)

from . import UserDBModel
from .BASE import BaseDBModel
from sqlalchemy.orm import relationship, foreign


class MedOrganizationDBModel(BaseDBModel):
    __tablename__ = "med_organizations"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    number = Column(Integer, nullable=False, unique=True)
    address = Column(Text, nullable=False)

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
