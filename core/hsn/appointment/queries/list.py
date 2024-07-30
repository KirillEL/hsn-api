from typing import Optional

from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, contains_eager, selectinload

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, BadRequestException, ValidationException
from core.hsn.appointment import Appointment
from core.hsn.appointment.schemas import (
    PatientAppointmentFlat,
    PatientFlatForAppointmentList,
)
from core.hsn.patient.commands.create import convert_to_patient_response
from shared.db.models import PatientDBModel, MedicinesPrescriptionDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import session
from pydantic import BaseModel, Field, ValidationError

from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


class HsnAppointmentListContext(BaseModel):
    user_id: int = Field(gt=0)

    limit: Optional[int] = None
    offset: Optional[int] = None


async def hsn_appointment_list(context: HsnAppointmentListContext):
    logger.info("Получение списка приемов...")
    results = []
    query = select(AppointmentDBModel).where(
        AppointmentDBModel.is_deleted.is_(False),
        AppointmentDBModel.doctor_id == context.user_id,
    )

    # query = query.outerjoin(AppointmentDBModel.block_clinic_doctor) \
    #     .outerjoin(AppointmentDBModel.block_clinical_condition) \
    #     .outerjoin(AppointmentDBModel.block_diagnose) \
    #     .outerjoin(AppointmentDBModel.block_ekg) \
    #     .outerjoin(AppointmentDBModel.block_complaint) \
    #     .outerjoin(AppointmentDBModel.block_laboratory_test) \
    #     .outerjoin(AppointmentDBModel.purposes) \
    #     .outerjoin(AppointmentDBModel.patient) \
    #     .outerjoin(PatientDBModel.contragent)
    #
    # query = query.options(selectinload(AppointmentDBModel.block_clinic_doctor),
    #                       selectinload(AppointmentDBModel.patient).selectinload(PatientDBModel.contragent),
    #                       selectinload(AppointmentDBModel.block_clinical_condition),
    #                       selectinload(AppointmentDBModel.block_diagnose),
    #                       selectinload(AppointmentDBModel.block_ekg),
    #                       selectinload(AppointmentDBModel.block_complaint),
    #                       selectinload(AppointmentDBModel.block_laboratory_test),
    #                       selectinload(AppointmentDBModel.purposes).selectinload(
    #                           AppointmentPurposeDBModel.medicine_prescription).selectinload(
    #                           MedicinesPrescriptionDBModel.medicine_group))

    query_count = (
        select(func.count(AppointmentDBModel.id))
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.doctor_id == context.user_id)
    )
    cursor_count = await session.execute(query_count)
    count_appointments = cursor_count.scalar()

    if context.limit is not None:
        query = query.limit(context.limit)
    if context.offset is not None:
        query = query.offset(context.offset)

    cursor = await session.execute(query)

    patient_appointments = cursor.unique().scalars().all()
    logger.debug(f"len_patient_appointments: {len(patient_appointments)}")
    if len(patient_appointments) == 0:
        raise NotFoundException(message="Приемы не найдены!")
    for appointment in patient_appointments:
        logger.debug(f"appointment: {appointment.__dict__}")
        logger.debug(f"appointment: {appointment.patient.contragent.__dict__}")
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

        appointment_flat = PatientAppointmentFlat(
            id=appointment.id,
            full_name=f'{patient_info.name} {patient_info.last_name} {patient_info.patronymic if patient_info.patronymic is not None else ""}'.rstrip(),
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
        results.append(appointment_flat)

    return {"data": results, "total": count_appointments}
