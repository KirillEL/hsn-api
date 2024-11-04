from loguru import logger
from pydantic import ValidationError
from sqlalchemy import select, RowMapping, Select, Result
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, ValidationException, BadRequestException, InternalServerException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.model import PatientAppointmentFlat, PatientFlatForAppointmentList
from shared.db.models import PatientDBModel, MedicinesPrescriptionDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


async def build_patient_info(appointment: RowMapping):
    appointment.patient.contragent.name = contragent_hasher.decrypt(appointment.patient.contragent.name)
    appointment.patient.contragent.last_name = contragent_hasher.decrypt(
        appointment.patient.contragent.last_name)
    if appointment.patient.contragent.patronymic:
        appointment.patient.contragent.patronymic = contragent_hasher.decrypt(
            appointment.patient.contragent.patronymic)

    patient_info = PatientFlatForAppointmentList(
        name=appointment.patient.contragent.name,
        last_name=appointment.patient.contragent.last_name,
        patronymic=appointment.patient.contragent.patronymic
    )
    return patient_info


@SessionContext()
async def hsn_appointment_by_id(
        doctor_id: int,
        appointment_id: int
) -> PatientAppointmentFlat:
    query: Select = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.is_deleted.is_(False),
               AppointmentDBModel.id == appointment_id)
    )

    query = (
        query.options(
            selectinload(AppointmentDBModel.block_clinic_doctor),
            selectinload(AppointmentDBModel.patient)
            .selectinload(PatientDBModel.contragent),
            selectinload(AppointmentDBModel.block_clinical_condition),
            selectinload(AppointmentDBModel.block_diagnose),
            selectinload(AppointmentDBModel.block_ekg),
            selectinload(AppointmentDBModel.block_complaint),
            selectinload(AppointmentDBModel.block_laboratory_test),
            selectinload(AppointmentDBModel.purposes)
            .selectinload(
                AppointmentPurposeDBModel.medicine_prescriptions
            )
            .selectinload(MedicinesPrescriptionDBModel.drug)
        )
    )

    cursor: Result = await db_session.execute(query)
    appointment: AppointmentDBModel = cursor.scalars().first()
    if not appointment:
        raise NotFoundException(message="Прием c id:{} не найден".format(appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            message="У вас нет прав для доступа к приему с id:{}".format(appointment_id)
        )

    patient_info = await build_patient_info(appointment)

    appointment_flat = PatientAppointmentFlat(
        id=appointment.id,
        full_name=f"{patient_info.last_name} {patient_info.name} {patient_info.patronymic}",
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
        status=appointment.status
    )
    return PatientAppointmentFlat.model_validate(appointment_flat)
