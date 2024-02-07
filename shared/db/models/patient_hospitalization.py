from sqlalchemy import BigInteger, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class PatientHospitalizationsDBModel(BaseDBModel):
    __tablename__ = 'patient_hospitalizations'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    patient_id = Column(BigInteger, ForeignKey('public.patients.id'))
    #patient = relationship('PatientDBModel', back_populates='patient_hospitalizations')

    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)


