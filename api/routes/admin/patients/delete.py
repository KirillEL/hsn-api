from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import delete


@admin_patient_router.delete(
    "/patients/{patient_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_delete(patient_id: int):
    await db_session.execute(delete(PatientDBModel).where(PatientDBModel.id == patient_id))
    return True
