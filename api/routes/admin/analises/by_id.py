from sqlalchemy import select
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext
from shared.db.models.analyses import AnalysesDBModel
from .router import admin_analises_router
from core.hsn.analise import Analise


@admin_analises_router.get(
    "/analises/{analise_id}",
    response_model=Analise,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_analise_by_id(analise_id: int):
    query = (
        select(AnalysesDBModel)
        .where(AnalysesDBModel.id == analise_id, AnalysesDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    analise = cursor.scalars().first()

    return Analise.model_validate(analise)
