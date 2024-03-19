from .BASE import BaseDBModel
from sqlalchemy import Column, Text, String, Float, ForeignKey, text, Integer, DateTime


class HormonalBloodAnalyseDBModel(BaseDBModel):
    __tablename__ = 'hormonal_blood_analyses'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    nt_pro_bnp = Column(Float)
    nt_pro_bnp_date = Column(DateTime(timezone=False))
    hba1c = Column(Float)
    hba1c_date = Column(DateTime(timezone=False))
