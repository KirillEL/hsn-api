from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
)
from shared.db import Transaction
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinical_condition import (
    AppointmentClinicalConditionBlockDBModel,
)
from shared.db.db_session import session
from shared.db.transaction import Propagation


class HsnBlockClinicalConditionUpdateContext(BaseModel):
    appointment_id: int
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


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_block_clinical_condition_update(
    context: HsnBlockClinicalConditionUpdateContext,
):
    payload = context.model_dump(exclude={"appointment_id"}, exclude_none=True)

    query = (
        select(AppointmentDBModel.block_clinical_condition_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor = await session.execute(query)
    block_clinical_condition_id = cursor.scalar()
    if block_clinical_condition_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_update = (
        update(AppointmentClinicalConditionBlockDBModel)
        .values(**payload)
        .where(
            AppointmentClinicalConditionBlockDBModel.id == block_clinical_condition_id
        )
        .returning(AppointmentClinicalConditionBlockDBModel)
    )
    cursor = await session.execute(query_update)
    updated_block = cursor.scalars().first()
    return AppointmentClinicalConditionBlock.model_validate(updated_block)
