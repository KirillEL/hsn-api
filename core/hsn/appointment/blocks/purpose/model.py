from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.user import UserAuthor


class AppointmentPurpose(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    medicine_prescription_id: int
    note: Optional[str] = None

    is_deleted: bool

    created_at: datetime
    created_by: UserAuthor

    updated_at: Optional[datetime] = None
    updated_by: Optional[UserAuthor] = None

    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserAuthor] = None


class MedicineGroupFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')

    id: int
    code: Optional[str] = None
    name: str
    note: Optional[str] = None


class MedicinePrescriptionFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    medicine_group: Optional[MedicineGroupFlat] = None
    name: str
    note: Optional[str] = None


class AppointmentPurposeFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appointment_id: int
    dosa: str
    note: Optional[str] = None
    medicine_prescription: MedicinePrescriptionFlat


class MedicineGroupData(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')

    id: int
    name: str
    dosa: str
    note: Optional[str] = None


class AppointmentPurposeResponseFlat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medicine_group: str
    medicine_group_data: Optional[MedicineGroupData] = None
