from sqlalchemy import Column, ForeignKey, DateTime, Date, BigInteger
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class SuppliedDiagnosesDBModel(BaseDBModel):
    __tablename__ = 'supplied_diagnoses'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_appointment_id = Column(BigInteger, ForeignKey('public.patient_appointments.id'), nullable=False)
    #patient_appointment = relationship('PatientAppointmentsDBModel', back_populates='supplied_diagnoses')

    diagnose_id = Column(BigInteger, ForeignKey('public.diagnoses_catalog.id'), nullable=False)
    #diagnose = relationship('DiagnosesCatalogDBModel', back_populates='supplied_diagnoses')

    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)

