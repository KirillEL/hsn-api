from sqlalchemy import select
from .router import admin_researchs_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.researchs import ResearchDBModel
from api.exceptions import ExceptionResponseSchema, NotFoundException
from core.hsn.research import Research


@admin_researchs_router.get(
    "/researchs/{research_id}",
    response_model="",
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_research_by_id(research_id: int):
    query = (
        select(ResearchDBModel)
        .where(ResearchDBModel.id == research_id, ResearchDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    research = cursor.scalars().first()
    if research is None:
        raise NotFoundException(message="исследование не найдено!")
    return Research.model_validate(research)
