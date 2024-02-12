from sqlalchemy import BigInteger, Column, Integer, String, text, Text, ForeignKey
from .BASE import BaseDBModel


class Analyses(BaseDBModel):
    __tablename__ = 'analyses'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    count_index = Column(Integer, nullable=False)
    patient_hospitalization_id = Column(BigInteger, ForeignKey('public.patient_hospitalizations.id'), nullable=False)
