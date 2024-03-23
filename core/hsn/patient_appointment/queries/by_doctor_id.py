from core.hsn.patient_appointment import PatientAppointment
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from shared.db.models.user import UserDBModel
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.doctor import DoctorDBModel
from shared.db.models.patient import PatientDBModel
from shared.db.models.patient_appointment import PatientAppointmentsDBModel
from loguru import logger


@SessionContext()
async def hsn_patient_appointment_get_by_doctor_id(doctor_id: int):
    query = (
        select(PatientAppointmentsDBModel)
        .where(PatientAppointmentsDBModel.doctor_id == doctor_id)
    )
    cursor = await db_session.execute(query)
    patient_appointments = cursor.scalars().all()

    return [PatientAppointment.model_validate(item) for item in patient_appointments]
