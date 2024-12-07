from sqlalchemy import Column, Boolean, Integer, text, Text
from domains.shared.db.models.BASE import BaseDBModel


class AppointmentComplaintBlockDBModel(BaseDBModel):
    __tablename__ = "appointment_block_complaints"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, nullable=False)
    has_fatigue = Column(Boolean, nullable=False, server_default=text("false"))
    rapid_heartbeat = Column(Boolean, nullable=False, server_default=text("false"))
    has_weakness = Column(Boolean, nullable=False, server_default=text("false"))
    has_dyspnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_orthopnea = Column(Boolean, nullable=False, server_default=text("false"))
    has_swelling_legs = Column(Boolean, nullable=False, server_default=text("false"))
    increased_ad = Column(Boolean, nullable=False, server_default=text("false"))
    heart_problems = Column(Boolean, nullable=False, server_default=text("false"))
    note = Column(Text)
