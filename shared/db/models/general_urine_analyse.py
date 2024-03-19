from .BASE import BaseDBModel
from sqlalchemy import Column, Integer, String, DateTime, text, ForeignKey, Float, Text


class GeneralUrineAnalyseDBModel(BaseDBModel):
    __tablename__ = 'general_urine_analyses'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    protein = Column(Float)
    protein_date = Column(DateTime(timezone=False))
    red_blood_cells = Column(Float)
    red_blood_cells_date = Column(DateTime(timezone=False))
    leukocytes = Column(Float)
    leukocytes_date = Column(DateTime(timezone=False))
    note = Column(Text)
