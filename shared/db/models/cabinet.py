from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean, text, DateTime
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class CabinetDBModel(BaseDBModel):
    __tablename__ = 'cabinets'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    number = Column(String(255), nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    med_id = Column(BigInteger, ForeignKey('public.med_organizations.id'))
    med_org = relationship("MedOrganizationDBModel", uselist=False)

    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    patients = relationship("PatientDBModel", back_populates="cabinet")
    doctors = relationship("DoctorDBModel", back_populates="cabinet")

    author_id = Column('created_by', Integer, nullable=False)
    created_by = relationship(UserDBModel,
                              primaryjoin=author_id == foreign(UserDBModel.id),
                              uselist=False,
                              viewonly=True,
                              lazy='selectin')

    editor_id = Column('updated_by', Integer)
    updated_by = relationship(UserDBModel,
                              primaryjoin=editor_id == foreign(UserDBModel.id),
                              uselist=False,
                              viewonly=True,
                              lazy='selectin')

    deleter_id = Column('deleted_by', Integer)
    deleted_by = relationship(UserDBModel,
                              primaryjoin=deleter_id == foreign(UserDBModel.id),
                              uselist=False,
                              viewonly=True,
                              lazy='selectin')
