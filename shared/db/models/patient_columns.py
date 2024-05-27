from sqlalchemy import JSON
from .BASE import BaseDBModel
from sqlalchemy import Column, String, Integer, ForeignKey


class PatientTableColumnsDBModel(BaseDBModel):
    __tablename__ = 'patient_columns'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('public.users.id'), nullable=False, unique=True)
    table_columns = Column(JSON, nullable=False)


