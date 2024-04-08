from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentComplaintBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    has_fatigue: Optional[bool] = False
    has_dyspnea: Optional[bool] = False
    has_swelling_legs: Optional[bool] = False
    has_weakness: Optional[bool] = False
    has_orthopnea: Optional[bool] = False
    has_heartbeat: Optional[bool] = True
    note: Optional[str] = None


class AppointmentBlockBooleanFieldsResponse(BaseModel):
    name: str
    displayName: str
    value: Optional[bool] = None