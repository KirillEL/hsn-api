from sqlalchemy import Column, Integer, String, BigInteger, Boolean, text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, foreign

from . import UserDBModel
from .BASE import BaseDBModel
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

distance_walkings = ('<200', '200-350', '350-500', '>500')


class ClinicalAssesmentDBModel(BaseDBModel):
    __tablename__ = "clinical_assesments"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    has_dyspnea = Column(Boolean, nullable=False, server_default=text("false"))
    distance_walking_6_minutes = Column(PGEnum(*distance_walkings, name='distance_walking_type', create_type=True),
                                        nullable=False)
    has_orthopnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_night_dyspnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_decreased_exercise_tolerance = Column(Boolean, nullable=False, server_default=text("false"))
    has_weakness = Column(Boolean, nullable=False, server_default=text("false"))
    has_increased_anknes = Column(Boolean, nullable=False, server_default=text("false"))
    has_night_cough = Column(Boolean, nullable=False, server_default=text("false"))
    has_weight_gain = Column(Boolean, nullable=False, server_default=text("false"))
    has_lose_weight = Column(Boolean, nullable=False, server_default=text("false"))
    has_depression = Column(Boolean, nullable=False, server_default=text("false"))
    has_increased_central_venous_pressure = Column(Boolean, nullable=False, server_default=text("false"))
    has_heartbeat = Column(Boolean, nullable=False, server_default=text("true"))
    has_hepatojugular_reflux = Column(Boolean, nullable=False, server_default=text("false"))
    has_third_ton = Column(Boolean, nullable=False, server_default=text("false"))
    has_displacement_of_the_apical = Column(Boolean, nullable=False, server_default=text("false"))
    has_peripheral_edema = Column(Boolean, nullable=False, server_default=text("false"))
    has_moist_rales = Column(Boolean, nullable=False, server_default=text("false"))
    has_heart_murmur = Column(Boolean, nullable=False, server_default=text("false"))
    has_tachycardia = Column(Boolean, nullable=False, server_default=text("false"))
    has_irregular_pulse = Column(Boolean, nullable=False, server_default=text("false"))
    has_tachypnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_hepatomegaly = Column(Boolean, nullable=False, server_default=text("false"))
    has_ascites = Column(Boolean, nullable=False, server_default=text("false"))
    has_cachexia = Column(Boolean, nullable=False, server_default=text("false"))

    patient_appointment_id = Column(BigInteger, ForeignKey("public.patient_appointments.id", ondelete="CASCADE"), nullable=False)
    patient_hospitalization_id = Column(BigInteger, ForeignKey("public.patient_hospitalizations.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(BigInteger, ForeignKey("public.patients.id", ondelete="CASCADE"), nullable=False)

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
