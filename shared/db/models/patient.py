from sqlalchemy import Column, String, BigInteger, Date, Text, ForeignKey, Boolean, text, DateTime, Integer
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.dialects.postgresql import ENUM as PGEnum


from . import UserDBModel
from .BASE import BaseDBModel
from enum import Enum


class Disability(Enum):
    NO_DISABILITY = "no"
    FIRST_DISABILITY = "1"
    SECOND_DISABILITY = "2"
    THIRD_DISABILITY = "3"


class LgotaDrugs(Enum):
    NO_LGOTA = "no"
    LGOTA = "yes"
    LGOTA_MONEY = "money"


class ClassificationFuncClasses(Enum):
    FK1 = "fk1"
    FK2 = "fk2"
    FK3 = "fk3"
    FK4 = "fk4"


class PatientDBModel(BaseDBModel):
    __tablename__ = 'patients'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    patronymic = Column(String(100))
    gender = Column(String(1), nullable=False)
    height = Column(Integer, nullable=False)
    main_diagnose = Column(Text)
    age = Column(Integer)
    disability = Column(PGEnum(Disability, name='disability', create_type=True), nullable=False,
                        server_default=text("'NO_DISABILITY'"))

    date_setup_diagnose = Column(DateTime)
    school_hsn_date = Column(DateTime)
    have_hospitalization = Column(Boolean, nullable=False, server_default=text("false"))
    count_hospitalizations = Column(Integer, nullable=False)
    lgota_drugs = Column(PGEnum(LgotaDrugs, name='lgota_drugs', create_type=True), nullable=False,
                         server_default=text("'NO_LGOTA'"))
    last_hospitalization_id = Column(BigInteger)  # подумать
    note = Column(Text, nullable=True)
    has_chronic_heart = Column(Boolean, nullable=False, server_default=text("false"))
    classification_func_classes = Column(PGEnum(ClassificationFuncClasses, name='classification_func_classes', create_type=True), server_default=text("'FK1'"))
    has_stenocardia = Column(Boolean, nullable=False, server_default=text("false"))
    has_arteria_hypertension = Column(Boolean, nullable=False, server_default=text("false"))
    arteria_hypertension_age = Column(Integer, nullable=True)

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
                              lazy='selectin')

    editor_id = Column('updated_by', Integer)
    updated_by = relationship(UserDBModel,
                              primaryjoin=editor_id == foreign(UserDBModel.id),
                              uselist=False,
                              lazy='selectin')

    deleter_id = Column('deleted_by', Integer)
    deleted_by = relationship(UserDBModel,
                              primaryjoin=deleter_id == foreign(UserDBModel.id),
                              uselist=False,
                              lazy='selectin')
