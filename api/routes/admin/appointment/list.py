from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from core.hsn.appointment.blocks.clinical_condition import AppointmentClinicalConditionBlock
from core.hsn.appointment.blocks.complaint import AppointmentComplaintBlock
from core.hsn.appointment.blocks.diagnose import AppointmentDiagnoseBlock
from core.hsn.appointment.blocks.ekg import AppointmentEkgBlock
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from core.user import UserAuthor
from shared.db import db_session
from shared.db.db_session import SessionContext, db_session
from shared.db.models import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from utils import contragent_hasher
from .router import admin_appointment_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request
from pydantic import BaseModel, ConfigDict


class AdminAppointmentDoctorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    phone_number: str
    is_glav: bool
    created_at: datetime
    created_by: UserAuthor


class AdminAppointmentPatientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')

    id: int
    name: str
    last_name: str
    patronymic: Optional[str] = None
    birth_date: str
    gender: str
    phone: str
    created_at: datetime
    created_by: UserAuthor


class AdminAppointmentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')

    id: int
    date: str
    date_next: Optional[str] = None
    status: str
    patient: AdminAppointmentPatientSchema
    doctor: AdminAppointmentDoctorSchema
    block_clinical_condition: Optional[AppointmentClinicalConditionBlock] = None
    block_diagnose: Optional[AppointmentDiagnoseBlock] = None
    block_laboratory_test: Optional[AppointmentLaboratoryTestBlock] = None
    block_ekg: Optional[AppointmentEkgBlock] = None
    block_complaint: Optional[AppointmentComplaintBlock] = None
    is_deleted: bool
    created_at: datetime
    created_by: UserAuthor


@admin_appointment_router.get(
    "/list",
    response_model=list[AdminAppointmentListResponse],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
@HandleExceptions()
async def admin_appointments_list(request: Request, limit: int = None, offset: int = None):
    query = (
        select(AppointmentDBModel)
        .options(
            selectinload(AppointmentDBModel.doctor),
            selectinload(AppointmentDBModel.patient).selectinload(PatientDBModel.cabinet),
            selectinload(AppointmentDBModel.patient).selectinload(PatientDBModel.contragent)
        )
        .where(AppointmentDBModel.is_deleted.is_(False))
    )

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    cursor = await db_session.execute(query)
    appointments = cursor.scalars().all()
    appointment_json = jsonable_encoder(appointments)
    logger.debug(f'{appointment_json}')
    model_array = []
    for appointment in appointments:
        model = AdminAppointmentListResponse(
            id=appointment.id,
            date=appointment.date,
            date_next=appointment.date_next if appointment.date_next else "",
            patient=AdminAppointmentPatientSchema(
                id=appointment.patient.id,
                name=contragent_hasher.decrypt(appointment.patient.contragent.name),
                last_name=contragent_hasher.decrypt(appointment.patient.contragent.last_name),
                patronymic=contragent_hasher.decrypt(
                    appointment.patient.contragent.patronymic) if appointment.patient.contragent.patronymic else "",
                gender=appointment.patient.gender,
                birth_date=contragent_hasher.decrypt(appointment.patient.contragent.birth_date) if appointment.patient.contragent.birth_date else "",
                phone=appointment.patient.phone,
                created_at=appointment.patient.created_at,
                created_by=appointment.patient.created_by
            ),
            doctor=AdminAppointmentDoctorSchema(
                id=appointment.doctor.id,
                name=appointment.doctor.name,
                last_name=appointment.doctor.last_name,
                patronymic=appointment.doctor.patronymic if appointment.doctor.patronymic else "",
                is_glav=appointment.doctor.is_glav,
                phone_number=appointment.doctor.phone_number,
                created_at=appointment.doctor.created_at,
                created_by=appointment.doctor.created_by
            ),
            status=appointment.status,
            block_ekg=appointment.block_ekg if appointment.block_ekg else None,
            block_diagnose=appointment.block_diagnose if appointment.block_diagnose else None,
            block_laboratory_test=appointment.block_laboratory_test if appointment.block_laboratory_test else None,
            block_clinical_condition=appointment.block_clinical_condition if appointment.block_clinical_condition else None,
            block_complaint=appointment.block_complaint if appointment.block_complaint else None,
            is_deleted=appointment.is_deleted,
            created_at=appointment.created_at,
            created_by=appointment.created_by
        )
        model_array.append(model)

    return model_array
