from sqlalchemy import Column, String, DateTime, Integer
from shared.db.models.BASE import BaseDBModel


class AppointmentDrugTherapyBlockDBModel(BaseDBModel):
    __tablename__ = 'appointment_block_drug_therapies'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    