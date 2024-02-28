from .router import admin_supplied_diagnose_router
from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.supplied_diagnoses import SuppliedDiagnosesDBModel
from core.hsn.supplied_diagnoses.model import SuppliedDiagnoses
from api.exceptions import ExceptionResponseSchema


@admin_supplied_diagnose_router.get(
    "/supplied_diagnoses",
    response_model=list[SuppliedDiagnoses],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_supplied_diagnoses_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(SuppliedDiagnosesDBModel)
        .where(SuppliedDiagnosesDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    cursor = await db_session.execute(query)
    supplied_diagnoses = cursor.scalars().all()

    return [SuppliedDiagnoses.model_validate(s_d) for s_d in supplied_diagnoses]
