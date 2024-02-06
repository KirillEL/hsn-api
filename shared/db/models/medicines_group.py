from sqlalchemy import Column, BigInteger, String
from .BASE import BaseDBModel


class MedicinesGroupDBModel(BaseDBModel):
    __tablename__ = 'medicines_group'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)

    
