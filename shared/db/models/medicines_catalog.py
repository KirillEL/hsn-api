from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class MedicinesCatalogDBModel(BaseDBModel):
    __tablename__ = 'medicines_catalog'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)

    group_id = Column(BigInteger, ForeignKey('public.medicines_group.id'), nullable=False)

    group = relationship('MedicinesGroupDBModel', back_populates='medicines_catalog')

