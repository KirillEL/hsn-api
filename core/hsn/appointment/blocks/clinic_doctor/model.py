from enum import Enum
from typing import Optional
from datetime import date as tdate
from pydantic import BaseModel, ConfigDict


class DisabilityType(Enum):
    NO = "нет"
    FIRST = "I"
    SECOND = "II"
    THIRD = "III"
    CANCEL = "отказ"


class LgotaDrugsType(Enum):
    YES = "да"
    NO = "нет"
    SSZ = "ССЗ"


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


class AppointmentClinicDoctorBlockResponse(AppointmentClinicDoctorBlock):
    model_config = ConfigDict(from_attributes=True, extra='ignore')
