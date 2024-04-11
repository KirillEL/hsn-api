from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class AppointmentBlockBooleanTextFieldsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    booleanName: str
    displayName: str
    textName: str
    booleanValue: Optional[bool] = None
    textValue: Optional[str] = None


class BaseTextDateField(BaseModel):
    textName: str
    displayName: str
    dateName: str
    textValue: Optional[str] = None
    dateValue: Optional[str] = None


class AppointmentBlockTextDateFieldsResponse(BaseTextDateField):
    model_config = ConfigDict(from_attributes=True)


class AppointmentBlockTextDateLaboratoryTestFieldsResponse(BaseModel):
    hormonal_blood_analysis: List[BaseTextDateField] = []
    general_blood_analysis: List[BaseTextDateField] = []
    blood_chemistry: List[BaseTextDateField] = []
    general_urine_analysis: List[BaseTextDateField] = []
