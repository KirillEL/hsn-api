from datetime import datetime
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions.base import ValidationErrorTelegramSendMessageSchema
from tg_api import tg_bot
from loguru import logger
from sqlalchemy import select, func, exc, Select, Result
from sqlalchemy.orm import joinedload, contains_eager, selectinload
from fastapi import Request
from api.exceptions import NotFoundException, BadRequestException, ValidationException, InternalServerException
from core.hsn.appointment import Appointment
from core.hsn.appointment.model import PatientAppointmentFlat, PatientFlatForAppointmentList
from core.hsn.patient.commands.create import convert_to_patient_response
from shared.db.models import PatientDBModel, MedicinesPrescriptionDBModel, DrugDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field, ValidationError

from shared.db.models.appointment.purpose import AppointmentPurposeDBModel
from utils import contragent_hasher


class HsnAppointmentListContext(BaseModel):
    doctor_id: int = Field(gt=0)

    limit: Optional[int] = Field(None, ge=1)
    offset: Optional[int] = Field(None, ge=0)


@SessionContext()
async def hsn_appointment_list(
        request: Request,
        context: HsnAppointmentListContext
):
    logger.info(f"Fetching appointments for doctor_id: {context.doctor_id}")

    query: Select = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.is_deleted.is_(False),
               AppointmentDBModel.doctor_id == context.doctor_id)
    )

    query = query.options(
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
        .selectinload(
            MedicinesPrescriptionDBModel.drug
        )
        .selectinload(DrugDBModel.drug_group)
    )

    query_count: Select = (
        select(func.count(AppointmentDBModel.id))
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.doctor_id == context.doctor_id)
    )
    cursor_count: Result = await db_session.execute(query_count)
    total_appointments: int = cursor_count.scalar()

    if context.limit:
        query = query.limit(context.limit)
    if context.offset:
        query = query.offset(context.offset)

    query = query.order_by(AppointmentDBModel.id.desc())

    try:
        cursor: Result = await db_session.execute(query)
        patient_appointments = cursor.unique().scalars().all()
    except exc.SQLAlchemyError as sqle:
        logger.error(f'Failed fetching patient appointments: {sqle}')
        message_model = ValidationErrorTelegramSendMessageSchema(
            message="*Не удалось получить список приемов*",
            doctor_id=context.doctor_id,
            doctor_name=request.user.doctor.name,
            doctor_last_name=request.user.doctor.last_name,
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            description=str(sqle)
        )
        tg_bot.send_message(
            message=str(message_model)
        )
        raise InternalServerException

    if not patient_appointments:
        logger.warning("No appointments found")
        return {"data": [], "total": 0}

    results: List[PatientAppointmentFlat] = []
    for appointment in patient_appointments:
        patient_info = PatientFlatForAppointmentList(
            name=contragent_hasher.decrypt(appointment.patient.contragent.name),
            last_name=contragent_hasher.decrypt(appointment.patient.contragent.last_name),
            patronymic=contragent_hasher.decrypt(
                appointment.patient.contragent.patronymic) if appointment.patient.contragent.patronymic else ""
        )

        appointment_flat = PatientAppointmentFlat(
            id=appointment.id,
            full_name=f'{patient_info.name} {patient_info.last_name} {patient_info.patronymic or ""}'.rstrip(),
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

    logger.info(f"Successfully fetched {len(results)} appointments")
    return {"data": results, "total": total_appointments}
