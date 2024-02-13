from pydantic import BaseModel, ConfigDict
from typing import Optional


class ClinicalAssesment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    has_dyspnea: Optional[bool] = False
    distance_walking_6_minutes: Optional[bool] = False
    has_orthopnea: Optional[bool] = False
    has_night_dyspnea: Optional[bool] = False
    has_decreased_exercise_tolerance: Optional[bool] = False
    has_weakness: Optional[bool] = False
    has_increased_anknes: Optional[bool] = False
    has_night_cough: Optional[bool] = False
    has_weight_gain: Optional[bool] = False
    has_lose_weight: Optional[bool] = False
    has_depression: Optional[bool] = False
    has_increased_central_venous_pressure: Optional[bool] = False
    has_heartbeat: Optional[bool] = True
    has_hepatojugular_reflux: Optional[bool] = False
    has_third_ton: Optional[bool] = False
    has_displacement_of_the_apical: Optional[bool] = False
    has_peripheral_edema: Optional[bool] = False
    has_moist_rales: Optional[bool] = False
    has_heart_murmur: Optional[bool] = False
    has_tachycardia: Optional[bool] = False
    has_irregular_pulse: Optional[bool] = False
    has_tachypnea: Optional[bool] = False
    has_hepatomegaly: Optional[bool] = False
    has_ascites: Optional[bool] = False
    has_cachexia: Optional[bool] = False

    patient_appointment_id: int
    patient_hospitalization_id: int
    patient_id: int
