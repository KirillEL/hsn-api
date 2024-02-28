from .router import admin_supplied_diagnose_router
from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.supplied_diagnoses import SuppliedDiagnosesDBModel
from core.hsn.supplied_diagnoses.model import SuppliedDiagnoses
from api.exceptions import ExceptionResponseSchema


@admin_supplied_diagnose_router.get(
    "/supplied_diagnoses/{supplied_diagnose_id}",
    response_model=SuppliedDiagnoses,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_supplied_diagnose_by_id(supplied_diagnose_id: int):
    query = (
        select(SuppliedDiagnosesDBModel)
        .where(SuppliedDiagnosesDBModel.id == supplied_diagnose_id, SuppliedDiagnosesDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    supplied_diagnose = cursor.scalars().first()

    return SuppliedDiagnoses.model_validate(supplied_diagnose)
