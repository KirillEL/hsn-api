from typing import Optional, Dict, Any

from pydantic import BaseModel
from sqlalchemy import insert, update, select

from api.exceptions.base import BlockAlreadyExistsException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import check_appointment_exists
from core.hsn.purpose.commands.create import check_appointment_exists
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel


class HsnBlockComplaintAndClinicalCondtionCreateContext(BaseModel):
    appointment_id: int

    has_fatigue: Optional[bool] = False
    has_dyspnea: Optional[bool] = False
    has_swelling_legs: Optional[bool] = False
    has_weakness: Optional[bool] = False
    has_orthopnea: Optional[bool] = False
    has_heartbeat: Optional[bool] = True
    note: Optional[str] = False

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

    def create_payloads(self) -> Dict[str, Dict[str, Any]]:
        symptoms_payload = {key: getattr(self, key) for key in [
            'has_fatigue', 'has_dyspnea', 'has_swelling_legs', 'has_weakness',
            'has_orthopnea', 'has_heartbeat', 'note'
        ]}

        clinical_conditions_payload = {key: getattr(self, key) for key in [
            'heart_failure_om', 'orthopnea', 'paroxysmal_nocturnal_dyspnea',
            'reduced_exercise_tolerance', 'weakness_fatigue', 'peripheral_edema',
            'ascites', 'hydrothorax', 'hydropericardium', 'night_cough',
            'weight_gain_over_2kg', 'weight_loss', 'depression', 'third_heart_sound',
            'apical_impulse_displacement_left', 'moist_rales_in_lungs',
            'heart_murmurs', 'tachycardia', 'irregular_pulse', 'tachypnea',
            'hepatomegaly', 'other_symptoms', 'height', 'weight', 'bmi', 'systolic_bp',
            'diastolic_bp', 'heart_rate', 'six_min_walk_distance'
        ]}

        return {
            "block_complaint": symptoms_payload,
            "clinical_condition": clinical_conditions_payload
        }


async def check_block_complaint_exists_in_appointment(appointment_id: int):
    query = (
        select(AppointmentDBModel.block_complaint_id)
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    block_complaint = cursor.scalar()
    if block_complaint:
        raise BlockAlreadyExistsException(message="Блок жалоб пациента уже присутствует у приема!")


async def check_block_clinical_condition_exists_in_appointment(appointment_id: int):
    query = (
        select(AppointmentDBModel.block_clinical_condition_id)
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    block_clinical_condition = cursor.scalar()
    if block_clinical_condition:
        raise BlockAlreadyExistsException(message="Блок клинического состояния уже присутствует у приема!")


@SessionContext()
async def hsn_block_complaint_and_clinical_condition_create(context: HsnBlockComplaintAndClinicalCondtionCreateContext):
    await check_appointment_exists(context.appointment_id)
    payloads = context.create_payloads()
    query_insert_block_complaint = (
        insert(AppointmentComplaintBlockDBModel)
        .values(payloads["block_complaint"])
        .returning(AppointmentComplaintBlockDBModel.id)
    )
    cursor = await db_session.execute(query_insert_block_complaint)
    new_block_complaint_id = cursor.scalar()
    await check_block_complaint_exists_in_appointment(new_block_complaint_id)

    query_insert_block_clinical_condidtion = (
        insert(AppointmentClinicalConditionBlockDBModel)
        .values(payloads["clinical_condition"])
        .returning(AppointmentClinicalConditionBlockDBModel.id)
    )
    cursor = await db_session.execute(query_insert_block_clinical_condidtion)
    new_block_clinical_condition_id = cursor.scalar()
    await check_block_clinical_condition_exists_in_appointment(new_block_clinical_condition_id)

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(
            block_complaint_id=new_block_complaint_id,
            block_clinical_condition_id=new_block_clinical_condition_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()

    return {
        "block_complaint_id": new_block_complaint_id,
        "block_clinical_condition_id": new_block_clinical_condition_id
    }
