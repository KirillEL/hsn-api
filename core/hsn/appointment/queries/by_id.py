from loguru import logger
from pydantic import ValidationError
from sqlalchemy import select, RowMapping
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import (
    NotFoundException,
    ValidationException,
    BadRequestException,
    InternalServerException,
)
from core.hsn.appointment.schemas import (
    PatientAppointmentFlat,
    PatientFlatForAppointmentList,
)
from shared.db.models import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import session
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


async def build_patient_info(appointment: RowMapping):
    appointment.patient.contragent.name = contragent_hasher.decrypt(
        appointment.patient.contragent.name
    )
    appointment.patient.contragent.last_name = contragent_hasher.decrypt(
        appointment.patient.contragent.last_name
    )
    if appointment.patient.contragent.patronymic:
        appointment.patient.contragent.patronymic = contragent_hasher.decrypt(
            appointment.patient.contragent.patronymic
        )

    patient_info = PatientFlatForAppointmentList(
        name=appointment.patient.contragent.name,
        last_name=appointment.patient.contragent.last_name,
        patronymic=appointment.patient.contragent.patronymic,
    )
    return patient_info


async def hsn_appointment_by_id(user_id: int, appointment_id: int):
    query = select(AppointmentDBModel).where(
        AppointmentDBModel.is_deleted.is_(False),
        AppointmentDBModel.doctor_id == user_id,
        AppointmentDBModel.id == appointment_id,
    )

    cursor = await session.execute(query)
    appointment = cursor.scalars().first()
    if not appointment:
        raise NotFoundException(message="Прием не найден!")

    patient_info = await build_patient_info(appointment)
    full_name = "{} {} {}".format(
        patient_info.last_name, patient_info.name, patient_info.patronymic
    )
    appointment_flat = PatientAppointmentFlat(
        id=appointment.id,
        full_name=full_name,
        doctor_id=appointment.doctor_id,
        date=appointment.date,
        date_next=str(appointment.date_next) if appointment.date_next else None,
        block_clinic_doctor=appointment.block_clinic_doctor,
        block_diagnose=appointment.block_diagnose,
        block_laboratory_test=appointment.block_laboratory_test,
        block_ekg=appointment.block_ekg,
        block_complaint=appointment.block_complaint,
        block_clinical_condition=appointment.block_clinical_condition,
        purposes=appointment.purposes,
        status=appointment.status,
    )
    return PatientAppointmentFlat.model_validate(appointment_flat)
