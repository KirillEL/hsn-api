from .BASE import BaseDBModel
from sqlalchemy import Column, Integer, String, Text, text, Float, ForeignKey, Boolean, DateTime


class AppointmentComplaintDBModel(BaseDBModel):
    __tablename__ = 'appointment_complaints'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, nullable=False)

    has_fatigue = Column(Boolean, nullable=False, server_default=text("false"))
    has_dyspnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_swelling_legs = Column(Boolean, nullable=False, server_default=text("false"))
    has_weakness = Column(Boolean, nullable=False, server_default=text("false"))
    has_orthopnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_heartbeat = Column(Boolean, nullable=False, server_default=text("true"))
    note_сomplaints = Column(Text)
    note_clinical = Column(Text)
    note_ekg = Column(Text)
    date_ekg = Column(DateTime(timezone=False))
    date_echo_ekg = Column(DateTime(timezone=False))
    fraction_out = Column(Float, nullable=False)
    sdla = Column(Float, nullable=False)