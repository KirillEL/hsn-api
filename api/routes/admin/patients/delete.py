from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import update
from fastapi import Request


@admin_patient_router.delete(
    "/patients/{patient_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_delete(patient_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }

    query = (
        update(PatientDBModel)
        .values(**payload)
        .where(PatientDBModel.id == patient_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True
