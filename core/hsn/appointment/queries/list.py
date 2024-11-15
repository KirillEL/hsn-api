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
from core.hsn.appointment.model import PatientAppointmentFlat, PatientFlatForAppointmentList, AppointmentsListDto
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
async def hsn_query_appointment_list(
        request: Request,
        context: HsnAppointmentListContext
):
    logger.info(f"Fetching appointments for doctor_id: {context.doctor_id}")

    query: Select = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.is_deleted.is_(False),
               AppointmentDBModel.doctor_id == context.doctor_id)
        .options(
            selectinload(AppointmentDBModel.patient)
            .selectinload(PatientDBModel.contragent)
        )
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

    cursor: Result = await db_session.execute(query)
    patient_appointments = cursor.unique().scalars().all()

    if not patient_appointments:
        logger.warning("No appointments found")
        return {"data": [], "total": 0}

    results: List[AppointmentsListDto] = []
    for appointment in patient_appointments:
        patient_info = PatientFlatForAppointmentList(
            name=contragent_hasher.decrypt(appointment.patient.contragent.name),
            last_name=contragent_hasher.decrypt(appointment.patient.contragent.last_name),
            patronymic=contragent_hasher.decrypt(
                appointment.patient.contragent.patronymic) if appointment.patient.contragent.patronymic else ""
        )

        appointment_flat = AppointmentsListDto(
            id=appointment.id,
            full_name=f'{patient_info.name} {patient_info.last_name} {patient_info.patronymic or ""}'.rstrip(),
            doctor_id=appointment.doctor_id,
            date=appointment.date,
            date_next=str(appointment.date_next) if appointment.date_next else None,
            status=appointment.status
        )
        results.append(appointment_flat)

    logger.info(f"Successfully fetched {len(results)} appointments")
    return {"data": results, "total": total_appointments}
