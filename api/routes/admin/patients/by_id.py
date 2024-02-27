from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import select


@admin_patient_router.get(
    "/patients/{patient_id}",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_by_id(patient_id: int):
    query = (
        select(PatientDBModel)
        .where(PatientDBModel.id == patient_id, PatientDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    patients = cursor.scalars().all()

    return [Patient.model_validate(p) for p in patients]
