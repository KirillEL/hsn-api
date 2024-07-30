from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentClinicalConditionBlock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    heart_failure_om: Optional[bool] = False
    orthopnea: Optional[bool] = False
    paroxysmal_nocturnal_dyspnea: Optional[bool] = False
    reduced_exercise_tolerance: Optional[bool] = False
    weakness_fatigue: Optional[bool] = False
    peripheral_edema: Optional[bool] = False
    ascites: Optional[bool] = False
    hydrothorax: Optional[bool] = False
    hydropericardium: Optional[bool] = False
    night_cough: Optional[bool] = False
    weight_gain_over_2kg: Optional[bool] = False
    weight_loss: Optional[bool] = False
    depression: Optional[bool] = False
    third_heart_sound: Optional[bool] = False
    apical_impulse_displacement_left: Optional[bool] = False
    moist_rales_in_lungs: Optional[bool] = False
    heart_murmurs: Optional[bool] = False
    tachycardia: Optional[bool] = False
    irregular_pulse: Optional[bool] = False
    tachypnea: Optional[bool] = False
    hepatomegaly: Optional[bool] = False
    other_symptoms: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[float] = None
    bmi: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate: Optional[int] = None
    six_min_walk_distance: Optional[int] = None


class AppointmentClinicalConditionBlockResponse(AppointmentClinicalConditionBlock):
    model_config = ConfigDict(from_attributes=True, extra='ignore')
