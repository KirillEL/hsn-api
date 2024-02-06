from sqlalchemy import Column, BigInteger, Integer, String, Boolean
from .BASE import BaseDBModel


class DiagnosesCatalogDBModel(BaseDBModel):
    __tablename__ = 'diagnoses_catalog'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)

    # add some


