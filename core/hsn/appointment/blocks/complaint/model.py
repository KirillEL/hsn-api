from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
)


class AppointmentComplaintBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: int
    has_fatigue: Optional[bool] = False
    has_dyspnea: Optional[bool] = False
    increased_ad: Optional[bool] = False
    rapid_heartbeat: Optional[bool] = False
    has_swelling_legs: Optional[bool] = False
    has_weakness: Optional[bool] = False
    has_orthopnea: Optional[bool] = False
    heart_problems: Optional[bool] = False
    note: Optional[str] = None


class AppointmentComplaintBlockResponse(AppointmentComplaintBlock):
    pass


class AppointmentBlockBooleanFieldsResponse(BaseModel):
    name: str
    displayName: str
    secondName: Optional[str]


class EchoEkgFieldsResponse(BaseModel):
    float_fields: list[AppointmentBlockBooleanFieldsResponse] = []
    boolean_fields: list[AppointmentBlockBooleanFieldsResponse] = []


class AppointmentBlockEkgBooleanFieldsResponse(BaseModel):
    ekg: list[AppointmentBlockBooleanFieldsResponse] = []
    echo_ekg: EchoEkgFieldsResponse = EchoEkgFieldsResponse()


class AppointmentComplaintWithClinicalCondition(BaseModel):
    block_complaint: Optional[AppointmentComplaintBlock] = None
    block_clinical_condition: Optional[AppointmentClinicalConditionBlock] = None


class AppointmentComplaintWithClinicalConditionResponse(
    AppointmentComplaintWithClinicalCondition
):
    pass
