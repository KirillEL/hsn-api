from sqlalchemy import Column, String, BigInteger, Date, Text, ForeignKey, Boolean, Enum, text, DateTime, Integer
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from . import UserDBModel
from .BASE import BaseDBModel

genders = ('male', 'female')
lgotadrugs = ('no', 'yes', 'money')


class PatientDBModel(BaseDBModel):
    __tablename__ = 'patients'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    patronymic = Column(String(255))
    gender = Column(PGEnum(*genders, name="gender_type", create_type=False), nullable=False)
    height = Column(Integer, nullable=False)
    age = Column(Integer)

    date_setup_diagnose = Column(DateTime, nullable=False)
    lgota_drugs = Column(PGEnum(*lgotadrugs, name="lgota_drugs_type", create_type=False), nullable=False)

    note = Column(Text, nullable=True)

    cabinet_id = Column(BigInteger, ForeignKey('public.cabinets.id'), nullable=False)

    cabinet = relationship("CabinetDBModel", back_populates="patients")

    contragent_id = Column(BigInteger, ForeignKey('public.contragents.id'), nullable=False, unique=True)

    contragent = relationship("ContragentDBModel", back_populates="patient", uselist=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

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
