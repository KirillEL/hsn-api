from sqlalchemy import select
from shared.db.db_session import SessionContext, db_session
from shared.db.models.patient_hospitalization import PatientHospitalizationsDBModel
from api.exceptions import ExceptionResponseSchema, NotFoundException
from .router import admin_patient_hospitalization_router
from core.hsn.patient_hospitalization import PatientHospitalization


@admin_patient_hospitalization_router.get(
    "/patient_hospitalizations/{patient_hospitalization_id}",
    response_model=PatientHospitalization,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_hospitalizations_by_id(patient_hospitalization_id: int):
    query = (
        select(PatientHospitalizationsDBModel)
        .where(PatientHospitalizationsDBModel.id == patient_hospitalization_id,
               PatientHospitalizationsDBModel.is_deleted.is_(False))
    )

    cursor = await db_session.execute(query)
    patient_hospitalization = cursor.scalars().first()
    if patient_hospitalization is None:
        raise NotFoundException(message="Госпитализация не найдена!")
    return PatientHospitalization.model_validate(patient_hospitalization)
