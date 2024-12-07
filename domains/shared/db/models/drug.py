from .BASE import BaseDBModel
from sqlalchemy import Column, Integer, BigInteger, Boolean, String, ForeignKey, text
from sqlalchemy.orm import relationship, foreign

from .drug_group import DrugGroupDBModel


class DrugDBModel(BaseDBModel):
    __tablename__ = "drugs"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    drug_group_id = Column(BigInteger, ForeignKey("public.drug_groups.id"))
    drug_group = relationship(
        DrugGroupDBModel,
        primaryjoin="foreign(DrugDBModel.drug_group_id) == DrugGroupDBModel.id",
    )
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
