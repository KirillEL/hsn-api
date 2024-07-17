from fastapi import HTTPException

from shared.db.db_session import db_session, SessionContext
from ..schemas import ClinicalAssesment
from sqlalchemy import insert, select
from pydantic import BaseModel, Field
from typing import Optional
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel


class HsnClinicalAssesmentCreateContext(BaseModel):
    user_id: int = Field(None, gt=0)

    has_dyspnea: Optional[bool] = False
    distance_walking_6_minutes: str
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


@SessionContext()
async def hsn_clinical_assesment_create(context: HsnClinicalAssesmentCreateContext) -> ClinicalAssesment:
    payload = context.model_dump(exclude={'user_id'})
    payload['author_id'] = context.user_id

    query_check_appointment_id = (
        select(ClinicalAssesmentDBModel)
        .where(ClinicalAssesmentDBModel.patient_appointment_id == context.patient_appointment_id)
    )
    cursor_1 = await db_session.execute(query_check_appointment_id)
    res = cursor_1.first()

    query_check_hositalization_id = (
        select(ClinicalAssesmentDBModel)
        .where(ClinicalAssesmentDBModel.patient_hospitalization_id == context.patient_hospitalization_id)
    )
    cursor_2 = await db_session.execute(query_check_hositalization_id)
    res_2 = cursor_2.first()

    query_check_patient_id = (
        select(ClinicalAssesmentDBModel)
        .where(ClinicalAssesmentDBModel.patient_id == context.patient_id)
    )
    cursor_3 = await db_session.execute(query_check_patient_id)
    res_3 = cursor_3.first()

    if res is None or res_2 is None or res_3 is None:
        raise HTTPException(status_code=400, detail="Упс что то пошло не так!")

    query = (
        insert(ClinicalAssesmentDBModel)
        .values(**payload)
        .returning(ClinicalAssesmentDBModel)
    )
    cursor = await db_session.execute(query)
    clinical_assesment = cursor.first()[0]
    return ClinicalAssesment.model_validate(clinical_assesment)


