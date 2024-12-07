from domains.core.hsn.appointment import Appointment
from domains.shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from domains.shared.db.models.appointment.appointment import AppointmentDBModel


@SessionContext()
async def hsn_patient_appointment_get_by_doctor_id(doctor_id: int):
    query = select(AppointmentDBModel).where(AppointmentDBModel.doctor_id == doctor_id)
    cursor = await db_session.execute(query)
    patient_appointments = cursor.scalars().all()

    return [Appointment.model_validate(item) for item in patient_appointments]
