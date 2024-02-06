from sqlalchemy import Column, BigInteger, String
from .BASE import BaseDBModel


class MedOrganizationDBModel(BaseDBModel):
    __tablename__ = 'med_organizations'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)

