from sqlalchemy import select, insert
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext
from shared.db.models.analyses import AnalysesDBModel
from .router import admin_analises_router
from core.hsn.analise import Analise
from pydantic import BaseModel, Field
from fastapi import Request


class CreateAnaliseDto(BaseModel):
    name: str = Field(max_length=255)
    count_index: int = Field(gt=0)
    patient_hospitalization_id: int = Field(gt=0)


@admin_analises_router.post(
    "/analises",
    response_model=Analise,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_analise_create(request: Request, dto: CreateAnaliseDto):
    query = (
        insert(AnalysesDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(AnalysesDBModel)
    )
    cursor = await db_session.execute(query)
    new_analise = cursor.scalars().first()

    return Analise.model_validate(new_analise)
