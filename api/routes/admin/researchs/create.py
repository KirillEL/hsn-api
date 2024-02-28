from datetime import datetime

from sqlalchemy import select, insert
from .router import admin_researchs_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.researchs import ResearchDBModel
from api.exceptions import ExceptionResponseSchema
from core.hsn.research import Research
from pydantic import BaseModel, Field
from fastapi import Request


class ResearchCreateDto(BaseModel):
    analyses_id: int = Field(gt=0)
    date: datetime
    patient_appointment_id: int = Field(gt=0)
    patient_hospitalization_id: int = Field(gt=0)


@admin_researchs_router.post(
    "/researchs",
    response_model=Research,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_research_create(request: Request, dto: ResearchCreateDto):
    query = (
        insert(ResearchDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(ResearchDBModel)
    )

    cursor = await db_session.execute(query)
    await db_session.commit()
    new_research = cursor.scalars().first()

    return Research.model_validate(new_research)
