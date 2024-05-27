from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from shared.db.models import PatientDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from utils import contragent_hasher
from . import AdminAppointmentListResponse, AdminAppointmentPatientSchema, AdminAppointmentDoctorSchema
from .router import admin_appointment_router
from api.exceptions import ExceptionResponseSchema, NotFoundException
from shared.db.db_session import db_session, SessionContext
from fastapi import Request


@admin_appointment_router.get(
	"/{appointment_id}",
	response_model=AdminAppointmentListResponse,
	responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
@HandleExceptions()
async def admin_appointment_get_by_id(request: Request, appointment_id: int):
	query = (
		select(AppointmentDBModel)
		.options(
			selectinload(AppointmentDBModel.doctor),
			selectinload(AppointmentDBModel.patient).selectinload(PatientDBModel.contragent),
			selectinload(AppointmentDBModel.block_ekg),
			selectinload(AppointmentDBModel.block_complaint),
			selectinload(AppointmentDBModel.block_diagnose),
			selectinload(AppointmentDBModel.block_laboratory_test),
			selectinload(AppointmentDBModel.block_clinical_condition)
		)
		.where(AppointmentDBModel.id == appointment_id)
	)
	cursor = await db_session.execute(query)
	appointment = cursor.scalars().first()
	if not appointment:
		raise NotFoundException(message="Нет такого приема!")

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
			birth_date=contragent_hasher.decrypt(
				appointment.patient.contragent.birth_date) if appointment.patient.contragent.birth_date else "",
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
	return model