from .BASE import BaseDBModel
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean


class AppointmentLaboratoryTestDBModel(BaseDBModel):
    __tablename__ = 'appointment_laboratory_tests'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    nt_pro_bnp = Column(Float)
    nt_pro_bnp_date = Column(DateTime)
    microalbumuria = Column(Float)
    microalbumuria_date = Column(DateTime)