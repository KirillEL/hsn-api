from .router import admin_cabinet_router
from sqlalchemy import insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.cabinet import CabinetDBModel
from core.hsn.cabinet import Cabinet
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from fastapi import Request


class CreateCabinetDto(BaseModel):
    number: str = Field(max_length=255)
    med_id: int = Field(gt=0)


@admin_cabinet_router.post(
    "/cabinets",
    response_model=Cabinet,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_cabinet_create(request: Request, dto: CreateCabinetDto):
    query = (
        insert(CabinetDBModel)
        .values(
            **dto.dict(),
            author_id=request.user.id
        )
        .returning(CabinetDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_cabinet = cursor.scalars().first()

    return Cabinet.model_validate(new_cabinet)
