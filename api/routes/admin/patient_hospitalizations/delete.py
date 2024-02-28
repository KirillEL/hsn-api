from sqlalchemy import select, update
from shared.db.db_session import SessionContext, db_session
from shared.db.models.patient_hospitalization import PatientHospitalizationsDBModel
from api.exceptions import ExceptionResponseSchema
from .router import admin_patient_hospitalization_router
from core.hsn.patient_hospitalization import PatientHospitalization
from fastapi import Request

@admin_patient_hospitalization_router.delete(
    "/patient_hospitalizations/{patient_hospitalization_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_hospitalization_delete(patient_hospitalization_id: int, request: Request):
    payload = {
        "is_deleted": True,
        "deleter_id": request.user.id
    }
    query = (
        update(PatientHospitalizationsDBModel)
        .values(
            **payload
        )
        .where(PatientHospitalizationsDBModel.id == patient_hospitalization_id)
    )
    await db_session.execute(query)
    return True
