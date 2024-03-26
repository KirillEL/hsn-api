from sqlalchemy import select

from .router import admin_patient_appointment_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient_appointment import PatientAppointmentsDBModel
from core.hsn.appointment import PatientAppointment
from api.exceptions import ExceptionResponseSchema


@admin_patient_appointment_router.get(
    "/patient_appointments",
    response_model=list[PatientAppointment],
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_appointment_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(PatientAppointmentsDBModel)
        .where(PatientAppointmentsDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(PatientAppointmentsDBModel.main_diagnose.contains(pattern))

    cursor = await db_session.execute(query)
    patient_appointments = cursor.scalars().all()

    return [PatientAppointment.model_validate(p_a) for p_a in patient_appointments]