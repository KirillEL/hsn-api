from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
)


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


class AppointmentComplaintBlockResponse(AppointmentComplaintBlock):
    model_config = ConfigDict(from_attributes=True, extra='ignore')


class AppointmentBlockBooleanFieldsResponse(BaseModel):
    name: str
    displayName: str


class EchoEkgFieldsResponse(BaseModel):
    integer_fields: list[AppointmentBlockBooleanFieldsResponse] = []
    boolean_fields: list[AppointmentBlockBooleanFieldsResponse] = []


class AppointmentBlockEkgBooleanFieldsResponse(BaseModel):
    ekg: list[AppointmentBlockBooleanFieldsResponse] = []
    echo_ekg: EchoEkgFieldsResponse = EchoEkgFieldsResponse()


class AppointmentComplaintWithClinicalCondition(BaseModel):
    block_complaint: AppointmentComplaintBlock
    block_clinical_condition: AppointmentClinicalConditionBlock
