from loguru import logger
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.exceptions import NotFoundException, ValidationException, BadRequestException
from core.hsn.appointment.model import PatientAppointmentFlat, PatientFlatForAppointmentList
from shared.db.models import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


@SessionContext()
async def hsn_appointment_by_id(user_id: int, appointment_id: int):
    try:
        query = select(AppointmentDBModel).where(AppointmentDBModel.is_deleted.is_(False),
                                                 AppointmentDBModel.doctor_id == user_id,
                                                 AppointmentDBModel.id == appointment_id)

        query = query.outerjoin(AppointmentDBModel.block_clinic_doctor) \
            .outerjoin(AppointmentDBModel.block_clinical_condition) \
            .outerjoin(AppointmentDBModel.block_diagnose) \
            .outerjoin(AppointmentDBModel.block_ekg) \
            .outerjoin(AppointmentDBModel.block_complaint) \
            .outerjoin(AppointmentDBModel.block_laboratory_test) \
            .outerjoin(AppointmentDBModel.purposes) \
            .outerjoin(AppointmentDBModel.patient) \
            .outerjoin(PatientDBModel.contragent)

        query = query.options(selectinload(AppointmentDBModel.block_clinic_doctor),
                              selectinload(AppointmentDBModel.patient).selectinload(PatientDBModel.contragent),
                              selectinload(AppointmentDBModel.block_clinical_condition),
                              selectinload(AppointmentDBModel.block_diagnose),
                              selectinload(AppointmentDBModel.block_ekg),
                              selectinload(AppointmentDBModel.block_complaint),
                              selectinload(AppointmentDBModel.block_laboratory_test),
                              selectinload(AppointmentDBModel.purposes).selectinload(
                                  AppointmentPurposeDBModel.medicine_prescription)
                              )

        cursor = await db_session.execute(query)
        appointment = cursor.scalars().first()
        if appointment is None:
            raise NotFoundException(message="Прием не найден!")

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

        appointment_flat = PatientAppointmentFlat(
            id=appointment.id,
            patient=patient_info,
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
    except ValidationError as ve:
        logger.error(f'Ошибка валидации приема: {ve}')
        raise ValidationException()
    except Exception as e:
        logger.error(f'Возникла ошибка: {e}')
        raise e
