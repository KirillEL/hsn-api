from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    text,
)


class DrugGroupDBModel(BaseDBModel):
    __tablename__ = "drug_groups"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)

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
