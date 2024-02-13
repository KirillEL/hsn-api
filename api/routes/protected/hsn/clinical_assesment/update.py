from typing import Optional
from fastapi import Request
from shared.db.models.clinical_assesment import DistanceWalking
from .router import clinical_assesment_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.clinical_assesment import ClinicalAssesment, HsnClinicalAssesmentUpdateContext, HsnClinicalAssesmentCreateContext
from pydantic import BaseModel, Field



class UpdateClinicalAssesmentRequest(BaseModel):
    has_dyspnea: Optional[bool] = Field(False, description="")
    distance_walking_6_minutes: str = Field(DistanceWalking.LOW.name, description="")
    has_orthopnea: Optional[bool] = Field(False, description="")
    has_night_dyspnea: Optional[bool] = Field(False, description="")
    has_decreased_exercise_tolerance: Optional[bool] = Field(False, description="")
    has_weakness: Optional[bool] = Field(False, description="")
    has_increased_anknes: Optional[bool] = Field(False, description="")
    has_night_cough: Optional[bool] = Field(False, description="")
    has_weight_gain: Optional[bool] = Field(False, description="")
    has_lose_weight: Optional[bool] = Field(False, description="")
    has_depression: Optional[bool] = Field(False, description="")
    has_increased_central_venous_pressure: Optional[bool] = Field(False, description="")
    has_heartbeat: Optional[bool] = Field(True, description="")
    has_hepatojugular_reflux: Optional[bool] = Field(False, description="")
    has_third_ton: Optional[bool] = Field(False, description="")
    has_displacement_of_the_apical: Optional[bool] = Field(False, description="")
    has_peripheral_edema: Optional[bool] = Field(False, description="")
    has_moist_rales: Optional[bool] = Field(False, description="")
    has_heart_murmur: Optional[bool] = Field(False, description="")
    has_tachycardia: Optional[bool] = Field(False, description="")
    has_irregular_pulse: Optional[bool] = Field(False, description="")
    has_tachypnea: Optional[bool] = Field(False, description="")
    has_hepatomegaly: Optional[bool] = Field(False, description="")
    has_ascites: Optional[bool] = Field(False, description="")
    has_cachexia: Optional[bool] = Field(False, description="")

    patient_appointment_id: int = Field(None, gt=0)
    patient_hospitalization_id: int = Field(None, gt=0)
    patient_id: int = Field(None, gt=0)


@clinical_assesment_router.put(
    "/{clinical_assesment_id}",
    response_model=ClinicalAssesment,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def hsn_clinical_assesment_update(clinical_assesment_id: int,request: Request, req_body: UpdateClinicalAssesmentRequest):
    context = HsnClinicalAssesmentUpdateContext(
        id=clinical_assesment_id,
        user_id=request.user.id,
        **req_body.dict()
    )
    return await hsn_clinical_assesment_update(context)

