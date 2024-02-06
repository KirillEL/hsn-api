from sqlalchemy import Column, Integer, String, BigInteger, Text
from .BASE import BaseDBModel


class ContragentDBModel(BaseDBModel):
    __tablename__ = 'contragents'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    phone_number = Column(BigInteger, unique=True, nullable=False)
    snils = Column(String(16), unique=True, nullable=False)

    address = Column(Text, nullable=False)
