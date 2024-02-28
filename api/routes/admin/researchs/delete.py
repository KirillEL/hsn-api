from sqlalchemy import select, update
from .router import admin_researchs_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.researchs import ResearchDBModel
from api.exceptions import ExceptionResponseSchema
from core.hsn.research import Research
from fastapi import Request


@admin_researchs_router.delete(
    "/researchs/{research_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_research_delete(research_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }

    query = (
        update(ResearchDBModel)
        .values(**payload)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True