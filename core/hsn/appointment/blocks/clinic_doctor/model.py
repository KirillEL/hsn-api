from typing import Optional
from datetime import date as tdate
from pydantic import BaseModel, ConfigDict


class AppointmentClinicDoctorBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reffering_doctor: Optional[str] = None
    reffering_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: bool
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[tdate] = None