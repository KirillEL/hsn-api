from sqlalchemy import Column, Integer, String, BigInteger
from .BASE import BaseDBModel


class ClinicalAssesmentDBModel(BaseDBModel):
    __tablename__ = "clinical_assesments"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    