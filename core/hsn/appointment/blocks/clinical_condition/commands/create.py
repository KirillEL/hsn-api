from typing import Optional

from sqlalchemy import insert, update, exc

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import check_appointment_exists
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinical_condition import AppointmentClinicalConditionBlockDBModel
from pydantic import BaseModel


class HsnAppointmentBlockClinicalConditionCreateContext(BaseModel):
    appointment_id: int
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
    try:
        await check_appointment_exists(context.appointment_id)
        payload = context.model_dump(exclude={'appointment_id'})
        query = (
            insert(AppointmentClinicalConditionBlockDBModel)
            .values(**payload)
            .returning(AppointmentClinicalConditionBlockDBModel.id)
        )
        cursor = await db_session.execute(query)
        new_block_clinical_condition_id = cursor.scalar()

        query_update_appointment = (
            update(AppointmentDBModel)
            .values(
                block_clinical_condition_id=new_block_clinical_condition_id
            )
            .where(AppointmentDBModel.id == context.appointment_id)
        )
        await db_session.execute(query_update_appointment)

        await db_session.commit()
        return new_block_clinical_condition_id
    except NotFoundException as ne:
        await db_session.rollback()
        raise ne
    except exc.SQLAlchemyError as sqle:
        await db_session.rollback()
        raise UnprocessableEntityException(message=str(sqle))
    except Exception as e:
        await db_session.rollback()
        raise InternalServerException(message=str(e))

