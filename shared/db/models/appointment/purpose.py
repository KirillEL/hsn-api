from sqlalchemy.orm import relationship, foreign

from .. import UserDBModel, MedicinesPrescriptionDBModel
from ..BASE import BaseDBModel
from sqlalchemy import Column, ForeignKey, Text, Integer, Boolean, text, DateTime, String


class AppointmentPurposeDBModel(BaseDBModel):
    __tablename__ = 'appointment_purposes'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)
    appointment_id = Column(Integer, ForeignKey('public.appointments.id'), nullable=False)
    appointment = relationship("AppointmentDBModel",
                               primaryjoin="AppointmentDBModel.id == AppointmentPurposeDBModel.appointment_id",
                               back_populates="purposes")
    # medicine_prescription_id = Column(Integer, ForeignKey('public.medicine_prescriptions.id'), nullable=False)
    # medicine_prescription = relationship(MedicinesPrescriptionDBModel, uselist=False)
    medicine_prescriptions = relationship(MedicinesPrescriptionDBModel)
    # dosa = Column(String(100), nullable=False)
    # note = Column(Text)

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
