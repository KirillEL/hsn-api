from sqlalchemy import Column, ForeignKey, String, BigInteger, Date
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class SuppliedMedicationsDBModel(BaseDBModel):
    __tablename__ = 'supplied_medications'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_appointment_id = Column(BigInteger, ForeignKey('public.patient_appointments.id'), nullable=False)
    patient_appointment = relationship('PatientAppointmentsDBModel', back_populates='supplied_diagnoses')

    medicine_id = Column(BigInteger, ForeignKey('public.medicines_catalog.id'), nullable=False)
    medicine = relationship('MedicinesCatalogDBModel', back_populates='supplied_medications')

    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
