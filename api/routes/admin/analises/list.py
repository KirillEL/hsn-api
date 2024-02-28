from sqlalchemy import select
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext
from shared.db.models.analyses import AnalysesDBModel
from .router import admin_analises_router
from core.hsn.analise import Analise

@admin_analises_router.get(
    "/analises",
    response_model=list[Analise],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_analises_list(limit: int = None, offset: int = None):
    query = (
        select(AnalysesDBModel)
        .where(AnalysesDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    cursor = await db_session.execute(query)
    analises = cursor.scalars().all()

    return [Analise.model_validate(a) for a in analises]