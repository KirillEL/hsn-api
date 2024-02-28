from sqlalchemy import select, update
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext
from shared.db.models.analyses import AnalysesDBModel
from .router import admin_analises_router
from core.hsn.analise import Analise
from fastapi import Request


@admin_analises_router.delete(
    "/analises/{analise_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_analise_delete(analise_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }
    query = (
        update(AnalysesDBModel)
        .values(**payload)
        .where(AnalysesDBModel.id == analise_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True
