from sqlalchemy import Column, String, BigInteger, ForeignKey,Text, Boolean, text, DateTime, Integer
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel


class MedicinesPrescriptionDBModel(BaseDBModel):
    __tablename__ = 'medicines_prescription'
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    medicine_group_id = Column(BigInteger, ForeignKey('public.medicines_group.id'), nullable=False)
    name = Column(Text, nullable=False)
    patient_appointment_id = Column(BigInteger, ForeignKey('public.patient_appointments.id'), nullable=False)
    patient_hospitalization_id = Column(BigInteger, ForeignKey('public.patient_hospitalizations.id'), nullable=False)

    mnn = Column()
    dosa = Column()
    note = Column(Text)


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
