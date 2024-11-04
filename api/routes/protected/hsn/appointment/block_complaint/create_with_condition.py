from typing import Optional

from pydantic import BaseModel, Field
from fastapi import Request

from core.hsn.appointment.blocks.complaint import hsn_command_block_complaint_and_clinical_condition_create, \
    HsnCommandBlockComplaintAndClinicalCondtionCreateContext
from .router import block_complaint_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException


class BlockComplaintCreateWithConditionResponse(BaseModel):
    block_complaint_id: int
    block_clinical_condition_id: int


class CreateBlockComplaintAndClinicalConditionRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
    has_fatigue: bool = Field(False)
    has_dyspnea: bool = Field(False)
    increased_ad: bool = Field(False)
    rapid_heartbeat: bool = Field(False)
    has_swelling_legs: bool = Field(False)
    has_weakness: bool = Field(False)
    has_orthopnea: bool = Field(False)
    note: str = Field(None, max_length=1000, examples=["Your note here"], description="Optional note, can be omitted.")

    #heart_failure_om: Optional[bool] = Field(False)
    orthopnea: Optional[bool] = Field(False)
    paroxysmal_nocturnal_dyspnea: Optional[bool] = Field(False)
    reduced_exercise_tolerance: Optional[bool] = Field(False)
    weakness_fatigue: Optional[bool] = Field(False)
    peripheral_edema: Optional[bool] = Field(False)
    ascites: Optional[bool] = Field(False)
    hydrothorax: Optional[bool] = Field(False)
    hydropericardium: Optional[bool] = Field(False)
    night_cough: Optional[bool] = Field(False)
    weight_gain_over_2kg: Optional[bool] = Field(False)
    weight_loss: Optional[bool] = Field(False)
    depression: Optional[bool] = Field(False)
    third_heart_sound: Optional[bool] = Field(False)
    apical_impulse_displacement_left: Optional[bool] = Field(False)
    moist_rales_in_lungs: Optional[bool] = Field(False)
    heart_murmurs: Optional[bool] = Field(False)
    tachycardia: Optional[bool] = Field(False)
    irregular_pulse: Optional[bool] = Field(False)
    tachypnea: Optional[bool] = Field(False)
    hepatomegaly: Optional[bool] = Field(False)
    other_symptoms: Optional[str] = Field(None, max_length=1000)

    height: Optional[int] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    bmi: Optional[float] = Field(None, gt=0)
    systolic_bp: Optional[int] = Field(None, gt=0)
    diastolic_bp: Optional[int] = Field(None, gt=0)
    heart_rate: Optional[int] = Field(None, gt=0)
    six_min_walk_distance: Optional[int] = Field(None, gt=0)


@block_complaint_router.post(
    "/create_with_condition",
    response_model=BlockComplaintCreateWithConditionResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_complaint_and_clinical_condition_route(
        request: Request,
        body: CreateBlockComplaintAndClinicalConditionRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandBlockComplaintAndClinicalCondtionCreateContext(
        **body.model_dump()
    )
    doctor_id: int = request.user.doctor.id
    return await hsn_command_block_complaint_and_clinical_condition_create(doctor_id, context)
