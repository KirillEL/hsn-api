from sqlalchemy import Column, BigInteger, String, DateTime, Float, ForeignKey, Text,text, Integer, Boolean
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class PatientAppointmentsDBModel(BaseDBModel):
    __tablename__ = 'patient_appointments'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_id = Column(BigInteger, ForeignKey('public.patients.id'))
    doctor_id = Column(BigInteger, ForeignKey('public.doctors.id'))
    cabinet_id = Column(BigInteger, ForeignKey('public.cabinets.id'))
    date = Column(DateTime(timezone=True), nullable=False)
    date_next = Column(DateTime(timezone=True), nullable=True)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    fv_lg = Column(Integer, nullable=False)
    main_diagnose = Column(Text, nullable=False)
    sistol_ad = Column(Float, nullable=False)
    diastal_ad = Column(Float, nullable=False)
    hss = Column(Integer, nullable=False)
    mit = Column(Float) # think about counting automatic
    has_fatigue = Column(Boolean, nullable=False, server_default=text("false"))
    has_dyspnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_swelling_legs = Column(Boolean, nullable=False, server_default=text("false"))
    has_weakness = Column(Boolean, nullable=False, server_default=text("false"))
    has_orthopnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_heartbeat = Column(Boolean, nullable=False, server_default=text("true"))
    note = Column(Text, nullable=True)


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


