from .router import block_clinical_condition_router
from api.exceptions import ExceptionResponseSchema, DoctorNotAssignedException
from pydantic import BaseModel, Field
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock, \
    hsn_command_appointment_block_clinical_condition_create, HsnCommandAppointmentBlockClinicalConditionCreateContext
from typing import Optional
from fastapi import Request


class CreateBlockClinicalConditionRequestBody(BaseModel):
    appointment_id: int = Field(gt=0)
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

    height: int = Field(gt=0)
    weight: float = Field(gt=0)
    bmi: Optional[float] = Field(None, gt=0)
    systolic_bp: int = Field(gt=0)
    diastolic_bp: int = Field(gt=0)
    heart_rate: int = Field(gt=0)
    six_min_walk_distance: Optional[str] = Field(max_length=40)


@block_clinical_condition_router.post(
    "/create",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def create_block_clinical_condition_route(
        request: Request,
        body: CreateBlockClinicalConditionRequestBody
):
    if not request.user.doctor:
        raise DoctorNotAssignedException

    context = HsnCommandAppointmentBlockClinicalConditionCreateContext(**body.model_dump())
    return await hsn_command_appointment_block_clinical_condition_create(context)
