from sqlalchemy import insert, select, Result
from sqlalchemy.sql.dml import ReturningInsert

from api.exceptions import NotFoundException, InternalServerException
from core.hsn.appointment import Appointment
from shared.db.models import BaseDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Type
from datetime import date as tdate
from shared.db.models.appointment.blocks.block_clinic_doctor import (
    AppointmentBlockClinicDoctorDBModel,
)
from shared.db.models.appointment.blocks.block_diagnose import (
    AppointmentDiagnoseBlockDBModel,
)
from shared.db.models.appointment.blocks.block_laboratory_test import (
    AppointmentLaboratoryTestBlockDBModel,
)
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from shared.db.models.appointment.blocks.block_complaint import (
    AppointmentComplaintBlockDBModel,
)
from shared.db.models.appointment.blocks.block_clinical_condition import (
    AppointmentClinicalConditionBlockDBModel,
)

DBModelType = TypeVar("DBModelType", bound=BaseDBModel)


class HsnCommandPatientAppointmentCreateContext(BaseModel):
    user_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)
    date: tdate
    date_next: Optional[tdate] = None
    block_clinic_doctor_id: int
    block_diagnose_id: int
    block_laboratory_test_id: int
    block_ekg_id: int
    block_complaint_id: int
    block_clinical_condition_id: int


async def check_block_exists(id: int, db_model: Type[DBModelType]):
    query = select(db_model).where(db_model.id == id)
    cursor = await db_session.execute(query)
    model = cursor.scalars().first()
    if model is not None:
        return model
    return None


async def check_block_clinic_doctor_exists(block_clinic_doctor_id: int):
    model = await check_block_exists(
        block_clinic_doctor_id, AppointmentBlockClinicDoctorDBModel
    )
    if model is None:
        raise NotFoundException(message="Блок клиника врач не найден")


async def check_block_diagnose_exists(block_diagnose_id: int):
    model = await check_block_exists(block_diagnose_id, AppointmentDiagnoseBlockDBModel)
    if model is None:
        raise NotFoundException(message="Блок диагноза не найден")


async def check_block_laboratory_test_exists(block_laboratory_test_id: int):
    model = await check_block_exists(
        block_laboratory_test_id, AppointmentLaboratoryTestBlockDBModel
    )
    if model is None:
        raise NotFoundException(message="Блок лабораторных тестов не найден")


async def check_block_ekg_exists(block_ekg_id: int):
    model = await check_block_exists(block_ekg_id, AppointmentEkgBlockDBModel)
    if model is None:
        raise NotFoundException(message="Блок екг не найден")


async def check_block_complaint_exists(block_complaint_id: int):
    model = await check_block_exists(
        block_complaint_id, AppointmentComplaintBlockDBModel
    )
    if model is None:
        raise NotFoundException(message="Блок жалоб не найден")


async def check_clinical_condition_exists(block_clinical_condition_id: int):
    model = await check_block_exists(
        block_clinical_condition_id, AppointmentClinicalConditionBlockDBModel
    )
    if model is None:
        raise NotFoundException(message="Блок клинического состояния не найден")


@SessionContext()
async def hsn_command_patient_appontment_create(
    context: HsnCommandPatientAppointmentCreateContext,
) -> Appointment:
    await check_block_clinic_doctor_exists(context.block_clinic_doctor_id)
    await check_block_diagnose_exists(context.block_diagnose_id)
    await check_block_laboratory_test_exists(context.block_laboratory_test_id)
    await check_block_ekg_exists(context.block_ekg_id)
    await check_block_complaint_exists(context.block_complaint_id)
    await check_clinical_condition_exists(context.block_clinical_condition_id)

    payload = context.model_dump(exclude={"user_id"})
    query: ReturningInsert = (
        insert(AppointmentDBModel)
        .values(author_id=context.doctor_id, **payload)
        .returning(AppointmentDBModel.id)
    )
    cursor: Result = await db_session.execute(query)
    await db_session.commit()
    new_appointment_id: int = cursor.scalar()
    return new_appointment_id
