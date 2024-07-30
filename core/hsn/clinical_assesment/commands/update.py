from sqlalchemy import update

from core.hsn.clinical_assesment import ClinicalAssesment
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel
from api.exceptions import NotFoundException


class HsnClinicalAssesmentUpdateContext(BaseModel):
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

    id: int = Field(None, gt=0)


@SessionContext()
async def hsn_clinical_assesment_update(context: HsnClinicalAssesmentUpdateContext):
    payload = context.model_dump(exclude={"user_id"})
    payload["author_id"] = context.user_id

    query = (
        update(ClinicalAssesmentDBModel)
        .values(**payload)
        .returning(ClinicalAssesmentDBModel)
    )
    cursor = await db_session.execute(query)
    res = cursor.first()
    if res is None:
        raise NotFoundException(message="не найден!")

    await db_session.commit()
    return ClinicalAssesment.model_validate(res[0])
