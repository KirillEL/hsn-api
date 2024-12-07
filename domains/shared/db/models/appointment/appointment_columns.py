from ..BASE import BaseDBModel
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, String, Text, Integer, ForeignKey


class AppointmentTableColumnsDBModel(BaseDBModel):
    __tablename__ = "appointment_columns"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("public.users.id"), nullable=False, unique=True
    )
    table_columns = Column(JSON, nullable=False)
