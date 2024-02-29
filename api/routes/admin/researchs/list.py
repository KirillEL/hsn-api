from sqlalchemy import select
from .router import admin_researchs_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.researchs import ResearchDBModel
from api.exceptions import ExceptionResponseSchema
from core.hsn.research import Research


@admin_researchs_router.get(
    "/researchs",
    response_model=list[Research],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_researchs_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(ResearchDBModel)
        .where(ResearchDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    cursor = await db_session.execute(query)
    researchs = cursor.unique().scalars().all()

    return [Research.model_validate(r) for r in researchs]
