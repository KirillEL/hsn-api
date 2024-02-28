from sqlalchemy import select
from shared.db.db_session import SessionContext, db_session
from shared.db.models.patient_hospitalization import PatientHospitalizationsDBModel
from api.exceptions import ExceptionResponseSchema
from .router import admin_patient_hospitalization_router
from core.hsn.patient_hospitalization import PatientHospitalization


@admin_patient_hospitalization_router.get(
    "/patient_hospitalizations",
    response_model=list[PatientHospitalization],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_hospitalization_list(limit: int = None, offset: int = None):
    query = (
        select(PatientHospitalizationsDBModel)
        .where(PatientHospitalizationsDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    cursor = await db_session.execute(query)
    patient_hospitalizations = cursor.scalars().all()

    return [PatientHospitalization.model_validate(p_h) for p_h in patient_hospitalizations]


