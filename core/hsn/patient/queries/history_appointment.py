from loguru import logger
from sqlalchemy import select, Result

from api.exceptions.base import ForbiddenException
from core.hsn.patient.model import PatientAppointmentHistoryDto
from shared.db.db_session import SessionContext, db_session
from shared.db.models import PatientDBModel, DoctorDBModel
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.queries import db_query_entity_by_id
from sqlalchemy import desc


@SessionContext()
async def hsn_query_patient_history_appointments(doctor_id: int, patient_id: int):
    patient_model: PatientDBModel = await db_query_entity_by_id(
        PatientDBModel, patient_id
    )
    doctor_model: DoctorDBModel = await db_query_entity_by_id(DoctorDBModel, doctor_id)

    if patient_model.cabinet_id != doctor_model.cabinet_id:
        raise ForbiddenException(
            "у вас нет прав для доступа к пациенту с id:{}".format(patient_model.id)
        )

    query = select(
        AppointmentDBModel.id.label("id"), AppointmentDBModel.date.label("date")
    ).where(
        AppointmentDBModel.patient_id == patient_model.id,
        AppointmentDBModel.doctor_id == doctor_model.id,
        AppointmentDBModel.is_deleted.is_(False),
    )
    query = query.order_by(desc(AppointmentDBModel.created_at))

    cursor: Result = await db_session.execute(query)
    appointments = cursor.all()
    if not appointments:
        return []

    result = [
        PatientAppointmentHistoryDto(id=appointment[0], date=appointment[1])
        for appointment in appointments
    ]

    return result
