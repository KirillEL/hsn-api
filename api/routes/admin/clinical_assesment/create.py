from .router import admin_clinical_assesment_router
from sqlalchemy import select, insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel
from core.hsn.clinical_assesment import ClinicalAssesment
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from fastapi import Request


class CreateClinicalAssesmentDto(BaseModel):
    patient_appointment_id: int = Field(gt=0)
    patient_hospitalization_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)

    has_dyspnea: bool = Field(False)
    distance_walking_6_minutes: str = Field("")
    has_orthopnea: bool = Field(False)
    has_night_dyspnea: bool = Field(False)
    has_decreased_exercise_tolerance: bool = Field(False)
    has_weakness: bool = Field(False)
    has_increased_anknes: bool = Field(False)
    has_night_cough: bool = Field(False)
    has_weight_gain: bool = Field(False)
    has_lose_weight: bool = Field(False)
    has_depression: bool = Field(False)
    has_increased_central_venous_pressure: bool = Field(False)
    has_heartbeat: bool = Field(True)
    has_hepatojugular_reflux: bool = Field(False)
    has_third_ton: bool = Field(False)
    has_displacement_of_the_apical: bool = Field(False)
    has_peripheral_edema: bool = Field(False)
    has_moist_rales: bool = Field(False)
    has_heart_murmur: bool = Field(False)
    has_tachycardia: bool = Field(False)
    has_irregular_pulse: bool = Field(False)
    has_tachypnea: bool = Field(False)
    has_hepatomegaly: bool = Field(False)
    has_ascites: bool = Field(False)
    has_cachexia: bool = Field(False)


@admin_clinical_assesment_router.post(
    "/clinical_assesments",
    response_model=ClinicalAssesment,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_clinical_assesment_create(request: Request, dto: CreateClinicalAssesmentDto):
    query = (
        insert(ClinicalAssesmentDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(ClinicalAssesmentDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_clinical_assesment = cursor.scalars().first()

    return ClinicalAssesment.model_validate(new_clinical_assesment)