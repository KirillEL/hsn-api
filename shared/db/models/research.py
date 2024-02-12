from sqlalchemy import Column, Integer, String, BigInteger
from .BASE import BaseDBModel


class ResearchDBModel(BaseDBModel):
    __tablename__ = 'research'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)