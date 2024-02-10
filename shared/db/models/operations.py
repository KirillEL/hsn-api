from sqlalchemy import Column, String, ForeignKey, BigInteger
from .BASE import BaseDBModel


class OperationsDBModel(BaseDBModel):
    __tablename__ = 'operations'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)