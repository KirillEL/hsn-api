from typing import Optional, Dict, Any, Type

from sqlalchemy import update, select, Select, Result
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.complaint.model import AppointmentComplaintWithClinicalCondition
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from pydantic import BaseModel, Field

from shared.db.queries import db_query_entity_by_id


class HsnCommandBlockComplaintAndClinicalConditionUpdateContext(BaseModel):
    user_id: int = Field(gt=0)
    appointment_id: int

    has_fatigue: Optional[bool] = None
    has_dyspnea: Optional[bool] = None
    has_swelling_legs: Optional[bool] = None
    has_weakness: Optional[bool] = None
    has_orthopnea: Optional[bool] = None
    has_heartbeat: Optional[bool] = None
    note: Optional[str] = None

    heart_failure_om: Optional[bool] = None
    orthopnea: Optional[bool] = None
    paroxysmal_nocturnal_dyspnea: Optional[bool] = None
    reduced_exercise_tolerance: Optional[bool] = None
    weakness_fatigue: Optional[bool] = None
    peripheral_edema: Optional[bool] = None
    ascites: Optional[bool] = None
    hydrothorax: Optional[bool] = None
    hydropericardium: Optional[bool] = None
    night_cough: Optional[bool] = None
    weight_gain_over_2kg: Optional[bool] = None
    weight_loss: Optional[bool] = None
    depression: Optional[bool] = None
    third_heart_sound: Optional[bool] = None
    apical_impulse_displacement_left: Optional[bool] = None
    moist_rales_in_lungs: Optional[bool] = None
    heart_murmurs: Optional[bool] = None
    tachycardia: Optional[bool] = None
    irregular_pulse: Optional[bool] = None
    tachypnea: Optional[bool] = None
    hepatomegaly: Optional[bool] = None
    other_symptoms: Optional[str] = None

    height: Optional[int] = None
    weight: Optional[float] = None
    bmi: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate: Optional[int] = None
    six_min_walk_distance: Optional[int] = None

    def create_payloads(self) -> Dict[str, Dict[str, Any]]:
        symptoms_keys = [
            'has_fatigue', 'has_dyspnea', 'has_swelling_legs', 'has_weakness',
            'has_orthopnea', 'has_heartbeat', 'note'
        ]
        clinical_conditions_keys = [
            'heart_failure_om', 'orthopnea', 'paroxysmal_nocturnal_dyspnea',
            'reduced_exercise_tolerance', 'weakness_fatigue', 'peripheral_edema',
            'ascites', 'hydrothorax', 'hydropericardium', 'night_cough',
            'weight_gain_over_2kg', 'weight_loss', 'depression', 'third_heart_sound',
            'apical_impulse_displacement_left', 'moist_rales_in_lungs',
            'heart_murmurs', 'tachycardia', 'irregular_pulse', 'tachypnea',
            'hepatomegaly', 'other_symptoms', 'height', 'weight', 'bmi', 'systolic_bp',
            'diastolic_bp', 'heart_rate', 'six_min_walk_distance'
        ]

        symptoms_payload = {
            key: getattr(self, key) for key in symptoms_keys if getattr(self, key) is not None
        }
        clinical_conditions_payload = {
            key: getattr(self, key) for key in clinical_conditions_keys if getattr(self, key) is not None
        }

        return {
            "block_complaint": symptoms_payload,
            "block_clinical_condition": clinical_conditions_payload
        }


@SessionContext()
async def hsn_command_block_complaint_and_clinical_condition_update(
        context: HsnCommandBlockComplaintAndClinicalConditionUpdateContext
) -> AppointmentComplaintWithClinicalCondition:
    user_id: int = context.user_id
    appointment_id: int = context.appointment_id
    payloads = context.create_payloads()
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)
    if not appointment:
        raise NotFoundException("Прием не найден")

    # 1
    query_get_block_complaint_id: Select = (
        select(AppointmentDBModel.block_complaint_id)
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query_get_block_complaint_id)
    block_complaint_id: int = cursor.scalar()
    if not block_complaint_id:
        raise NotFoundException(message="У приема не привязан еще блок жалоб!")

    query_get_block_clinical_condition_id: Select = (
        select(AppointmentDBModel.block_clinical_condition_id)
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query_get_block_clinical_condition_id)
    block_clinical_condition_id: int = cursor.scalar()
    if not block_clinical_condition_id:
        raise NotFoundException(message="У приема не привязан еще блок клинического состояния!")

    query_update_block_complaint: ReturningUpdate = (
        update(AppointmentComplaintBlockDBModel)
        .values(payloads["block_complaint"])
        .where(AppointmentComplaintBlockDBModel.id == block_complaint_id)
        .returning(AppointmentComplaintBlockDBModel)
    )
    cursor: Result = await db_session.execute(query_update_block_complaint)
    updated_block_complaint = cursor.scalars().first()

    query_update_block_clinical_condition: ReturningUpdate = (
        update(AppointmentClinicalConditionBlockDBModel)
        .values(payloads["block_clinical_condition"])
        .where(AppointmentClinicalConditionBlockDBModel.id == block_clinical_condition_id)
        .returning(AppointmentClinicalConditionBlockDBModel)
    )
    cursor: Result = await db_session.execute(query_update_block_clinical_condition)
    updated_block_clinical_condition = cursor.scalars().first()

    await db_session.commit()
    response = AppointmentComplaintWithClinicalCondition(
        block_complaint=updated_block_complaint,
        block_clinical_condition=updated_block_clinical_condition
    )
    return AppointmentComplaintWithClinicalCondition.model_validate(response)
