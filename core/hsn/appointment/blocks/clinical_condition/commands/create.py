from typing import Optional

from sqlalchemy import insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from pydantic import BaseModel

class HsnAppointmentBlockClinicalConditionCreateContext(BaseModel):
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
    other_symptoms: Optional[str] = False

    height: Optional[int] = None
    weight: Optional[float] = None
    bmi: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate: Optional[int] = None
    six_min_walk_distance: Optional[int] = None

@SessionContext()
async def hsn_appointment_block_clinical_condition_create(context: HsnAppointmentBlockClinicalConditionCreateContext):
    query = (
        insert(AppointmentClinicalConditionBlockDBModel)
        .values(**context.model_dump())
        .returning(AppointmentClinicalConditionBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_block_clinical_condition_id = cursor.scalar()
    return new_block_clinical_condition_id