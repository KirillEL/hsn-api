from sqlalchemy import Column, BigInteger, String, Boolean, text
from .BASE import BaseDBModel
from sqlalchemy.orm import relationship


class MedOrganizationDBModel(BaseDBModel):
    __tablename__ = 'med_organizations'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    #cabinets = relationship("CabinetDBModel", back_populates="med_organization")