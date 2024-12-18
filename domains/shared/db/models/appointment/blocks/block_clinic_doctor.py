from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    text,
    Boolean,
    DateTime,
)
from domains.shared.db.models.BASE import BaseDBModel


class AppointmentBlockClinicDoctorDBModel(BaseDBModel):
    __tablename__ = "appointment_block_clinic_doctors"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, nullable=False)
    referring_doctor = Column(Text)
    referring_clinic_organization = Column(Text)
    disability = Column(
        String(50), nullable=False, server_default=text("'нет'::character varying")
    )
    lgota_drugs = Column(
        String(50), nullable=False, server_default=text("'нет'::character varying")
    )
    has_hospitalization = Column(Boolean, nullable=False, server_default=text("false"))
    count_hospitalization = Column(Integer)
    last_hospitalization_date = Column(DateTime(timezone=False))
