from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import select
from sqlalchemy.orm import joinedload


@admin_patient_router.get(
    "/patients",
    response_model=list[Patient],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patients_list(limit: int = None, offset: int = None, pattern:str = None):
    query = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.contragent))
        .where(PatientDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(PatientDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    patients = cursor.scalars().all()

    return [Patient.model_validate(patient) for patient in patients]

