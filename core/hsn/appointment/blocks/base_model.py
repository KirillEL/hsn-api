from typing import Optional

from pydantic import BaseModel, ConfigDict

class AppointmentBlockBooleanTextFieldsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    booleanName: str
    displayName: str
    textName: str
    booleanValue: Optional[bool] = None
    textValue: Optional[str] = None


class AppointmentBlockTextDateFieldsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    textName: str
    displayName: str
    dateName: str
    textValue: Optional[str] = None
    dateValue: Optional[str] = None