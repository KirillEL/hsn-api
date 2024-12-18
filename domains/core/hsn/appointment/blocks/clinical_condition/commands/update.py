from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update, Select, Result
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from domains.core.hsn.appointment.blocks.clinical_condition import (
    AppointmentClinicalConditionBlock,
)
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from domains.shared.db.models.appointment.blocks.block_clinical_condition import (
    AppointmentClinicalConditionBlockDBModel,
)
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.queries import db_query_entity_by_id


class HsnCommandBlockClinicalConditionUpdateContext(BaseModel):
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


@SessionContext()
async def hsn_command_block_clinical_condition_update(
    doctor_id: int, context: HsnCommandBlockClinicalConditionUpdateContext
) -> AppointmentClinicalConditionBlock:
    payload = context.model_dump(exclude={"appointment_id"}, exclude_none=True)

    appointment = await db_query_entity_by_id(
        AppointmentDBModel, context.appointment_id
    )

    if not appointment:
        raise NotFoundException(
            "Прием с id: {} не найден".format(context.appointment_id)
        )

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            "У вас нет доступа к приему с id: {}".format(context.appointment_id)
        )

    query: Select = (
        select(AppointmentDBModel.block_clinical_condition_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_clinical_condition_id: int = cursor.scalar()

    if not block_clinical_condition_id:
        raise NotFoundException(
            message="У приема c id:{} нет данного блока".format(context.appointment_id)
        )

    query_update: ReturningUpdate = (
        update(AppointmentClinicalConditionBlockDBModel)
        .values(**payload)
        .where(
            AppointmentClinicalConditionBlockDBModel.id == block_clinical_condition_id
        )
        .returning(AppointmentClinicalConditionBlockDBModel)
    )
    cursor: Result = await db_session.execute(query_update)
    await db_session.commit()
    updated_block: AppointmentClinicalConditionBlockDBModel = cursor.scalars().first()
    return AppointmentClinicalConditionBlock.model_validate(updated_block)
