from ..BASE import BaseDBModel
from sqlalchemy import Column, ForeignKey, Text, Integer


class AppointmentPurposeDBModel(BaseDBModel):
    __tablename__ = 'appointment_purposes'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    appointment_id = Column(Integer, ForeignKey('public.appointments.id'), nullable=False)
    medicine_prescription_id = Column(Integer, ForeignKey('public.medicine_prescriptions.id'), nullable=False)
    note = Column(Text)

