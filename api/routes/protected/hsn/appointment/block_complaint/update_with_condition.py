from typing import Optional

from pydantic import BaseModel, Field

from core.hsn.appointment.blocks.complaint import HsnBlockComplaintAndClinicalConditionUpdateContext, \
    hsn_block_complaint_and_clinical_condition_update
from core.hsn.appointment.blocks.complaint.model import AppointmentComplaintWithClinicalCondition
from .router import block_complaint_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


class UpdateBlockComplaintAndClinicalConditionRequestBody(BaseModel):
    has_fatigue: Optional[bool] = Field(None)
    has_dyspnea: Optional[bool] = Field(None)
    has_swelling_legs: Optional[bool] = Field(None)
    has_weakness: Optional[bool] = Field(None)
    has_orthopnea: Optional[bool] = Field(None)
    has_heartbeat: Optional[bool] = Field(None)
    note: Optional[str] = Field(None, max_length=1000, examples=["Your note here"], description="Optional note, can be omitted.")

    heart_failure_om: Optional[bool] = Field(None)
    orthopnea: Optional[bool] = Field(None)
    paroxysmal_nocturnal_dyspnea: Optional[bool] = Field(None)
    reduced_exercise_tolerance: Optional[bool] = Field(None)
    weakness_fatigue: Optional[bool] = Field(None)
    peripheral_edema: Optional[bool] = Field(None)
    ascites: Optional[bool] = Field(None)
    hydrothorax: Optional[bool] = Field(None)
    hydropericardium: Optional[bool] = Field(None)
    night_cough: Optional[bool] = Field(None)
    weight_gain_over_2kg: Optional[bool] = Field(None)
    weight_loss: Optional[bool] = Field(None)
    depression: Optional[bool] = Field(None)
    third_heart_sound: Optional[bool] = Field(None)
    apical_impulse_displacement_left: Optional[bool] = Field(None)
    moist_rales_in_lungs: Optional[bool] = Field(None)
    heart_murmurs: Optional[bool] = Field(None)
    tachycardia: Optional[bool] = Field(None)
    irregular_pulse: Optional[bool] = Field(None)
    tachypnea: Optional[bool] = Field(None)
    hepatomegaly: Optional[bool] = Field(None)
    other_symptoms: Optional[str] = Field(None, max_length=1000)

    height: Optional[int] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    bmi: Optional[float] = Field(None, gt=0)
    systolic_bp: Optional[int] = Field(None, gt=0)
    diastolic_bp: Optional[int] = Field(None, gt=0)
    heart_rate: Optional[int] = Field(None, gt=0)
    six_min_walk_distance: Optional[int] = Field(None, gt=0)

@block_complaint_router.patch(
    "/update_with_condition/{appointment_id}",
    response_model=AppointmentComplaintWithClinicalCondition,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def update_block_complaint_and_clinical_condition(request: Request, appointment_id: int, body: UpdateBlockComplaintAndClinicalConditionRequestBody):
    context = HsnBlockComplaintAndClinicalConditionUpdateContext(
        user_id=request.user.id,
        appointment_id=appointment_id,
        **body.model_dump()
    )
    return await hsn_block_complaint_and_clinical_condition_update(context)