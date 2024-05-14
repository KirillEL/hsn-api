from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import joinedload, contains_eager, selectinload

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, BadRequestException, ValidationException
from core.hsn.appointment import Appointment
from core.hsn.appointment.model import PatientAppointmentFlat, PatientFlatForAppointmentList
from core.hsn.patient.commands.create import convert_to_patient_response
from shared.db.models import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field, ValidationError

from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


class HsnAppointmentListContext(BaseModel):
    user_id: int = Field(gt=0)

    limit: Optional[int] = None
    offset: Optional[int] = None


@SessionContext()
@HandleExceptions()
async def hsn_appointment_list(context: HsnAppointmentListContext):
    logger.info("Получение списка приемов...")
    results = []
    query = select(AppointmentDBModel).where(AppointmentDBModel.is_deleted.is_(False),
                                             AppointmentDBModel.doctor_id == context.user_id)

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
                              AppointmentPurposeDBModel.medicine_prescription))

    if context.limit is not None:
        query = query.limit(context.limit)
    if context.offset is not None:
        query = query.offset(context.offset)

    cursor = await db_session.execute(query)

    patient_appointments = cursor.unique().scalars().all()
    for appointment in patient_appointments:
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
        results.append(appointment_flat)

    return results
