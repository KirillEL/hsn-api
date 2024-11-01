from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class AppointmentBlockBooleanTextFieldsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    booleanName: str
    displayName: str
    textName: str


class BaseTextDateField(BaseModel):
    textName: str
    displayName: str
    dateName: list[str] = []


class BaseTextField(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    textName: str
    displayName: str


class HormonalBloodAnalysisTextDateField(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    textName: str
    displayName: str
    dateName: str


class GeneralBloodAnalysisTextDateField(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fields: list[BaseTextField]
    dateName: str


class BloodChemistryTextDateField(GeneralBloodAnalysisTextDateField):
    pass


class GeneralUrineAnalysisTextDateField(GeneralBloodAnalysisTextDateField):
    pass


class AppointmentBlockTextDateFieldsResponse(BaseTextDateField):
    model_config = ConfigDict(from_attributes=True)


class AppointmentBlockTextDateLaboratoryTestFieldsResponse(BaseModel):
    hormonal_blood_analysis: List[HormonalBloodAnalysisTextDateField] = []
    general_blood_analysis: Optional[GeneralBloodAnalysisTextDateField] = None
    blood_chemistry: Optional[BloodChemistryTextDateField] = None
    general_urine_analysis: Optional[GeneralUrineAnalysisTextDateField] = None
