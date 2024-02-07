from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship
from .BASE import BaseDBModel


class CabinetDBModel(BaseDBModel):
    __tablename__ = 'cabinets'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    med_id = Column(BigInteger, ForeignKey('public.med_organizations.id'))

    #med_organization = relationship('MedOrganizationDBModel', back_populates="cabinets")
    #doctor = relationship("DoctorDBModel", back_populates="cabinet")