from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class PatientAppointment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    doctor_id: int
    cabinet_id: int

    date: datetime

    weight: float
    height: float

    is_deleted: bool
    created_at: datetime
    created_by: str

    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None

