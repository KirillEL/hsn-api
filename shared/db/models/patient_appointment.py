from sqlalchemy import Column, BigInteger, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class PatientAppointmentsDBModel(BaseDBModel):
    __tablename__ = 'patient_appointments'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_id = Column(BigInteger, ForeignKey('public.patients.id'))
    doctor_id = Column(BigInteger, ForeignKey('public.doctors.id'))
    cabinet_id = Column(BigInteger, ForeignKey('public.cabinets.id'))

    patient = relationship('PatientDBModel', back_populates="patient_appointments")
    doctor = relationship('DoctorDBModel', back_populates="patient_appointments")
    cabinet = relationship('CabinetDBModel', back_populates="patient_appointments")

    date = Column(DateTime, nullable=False)

    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)


