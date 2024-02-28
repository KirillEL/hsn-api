from .router import admin_supplied_diagnose_router
from sqlalchemy import select, update
from shared.db.db_session import db_session, SessionContext
from shared.db.models.supplied_diagnoses import SuppliedDiagnosesDBModel
from core.hsn.supplied_diagnoses.model import SuppliedDiagnoses
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@admin_supplied_diagnose_router.delete(
    "/supplied_diagnoses/{supplied_diagnose_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_supplied_diagnose_delete(supplied_diagnose_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }
    query = (
        update(SuppliedDiagnosesDBModel)
        .values(**payload)
        .where(SuppliedDiagnosesDBModel.id == supplied_diagnose_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True
