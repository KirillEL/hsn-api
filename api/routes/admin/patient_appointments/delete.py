from sqlalchemy import select, delete

from .router import admin_patient_appointment_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient_appointment import PatientAppointmentsDBModel
from core.hsn.appointment import PatientAppointment
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@admin_patient_appointment_router.delete(
    "/patient_appointments/{patient_appointment_id}",
    response_model=bool,
    responses={"400": {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_appointment_delete(patient_appointment_id: int, request: Request):
    query = (
        delete(PatientAppointmentsDBModel)
        .where(PatientAppointmentsDBModel.id == patient_appointment_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True
