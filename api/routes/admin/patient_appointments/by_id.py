from sqlalchemy import select

from .router import admin_patient_appointment_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient_appointment import PatientAppointmentsDBModel
from core.hsn.appointment import PatientAppointment
from api.exceptions import ExceptionResponseSchema, NotFoundException


@admin_patient_appointment_router.get(
    "/patient_appointment/{patient_appointment_id}",
    response_model=PatientAppointment,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_appointment_by_id(patient_appointment_id: int):
    query = (
        select(PatientAppointmentsDBModel)
        .where(PatientAppointmentsDBModel.id == patient_appointment_id, PatientAppointmentsDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    patient_appointment = cursor.scalars().first()
    if patient_appointment is None:
        raise NotFoundException(message="Прием не найден!")
    return PatientAppointment.model_validate(patient_appointment)

