from .BASE import BaseDBModel
from sqlalchemy import Column, Integer, String, Float, DateTime, text


class GeneralBloodAnalyseDBModel(BaseDBModel):
    __tablename__ = 'general_blood_analyses'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    gemoglobin = Column(Float)
    gemoglobin_date = Column(DateTime(timezone=False))
