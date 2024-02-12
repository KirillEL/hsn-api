from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime
from .BASE import BaseDBModel


class ResearchDBModel(BaseDBModel):
    __tablename__ = 'researchs'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    analyses_id = Column(BigInteger, ForeignKey('public.analyses.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    patient_appointment_id = Column(BigInteger, ForeignKey('public.patient_appointments.id'), nullable=False)
    patient_hospitalization_id = Column(BigInteger, ForeignKey('public.patient_hospitalizations.id'), nullable=False)
