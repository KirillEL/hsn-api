from .router import admin_cabinet_router
from sqlalchemy import insert, select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.med_organization import MedOrganizationDBModel
from core.hsn.cabinet import Cabinet
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from fastapi import Request, HTTPException
from api.exceptions import NotFoundException


class CreateCabinetDto(BaseModel):
    number: str = Field(max_length=255)
    med_id: int = Field(gt=0)

async def check_med_org_exist(med_id: int) -> None:
    query = (
        select(MedOrganizationDBModel)
        .where(MedOrganizationDBModel.id == med_id, MedOrganizationDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    med_org = cursor.scalars().first()
    if med_org is None:
        raise NotFoundException(message="Мед учреждение не найдено !")


@admin_cabinet_router.post(
    "/cabinets",
    response_model=Cabinet,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_cabinet_create(request: Request, dto: CreateCabinetDto):
    try:
        await check_med_org_exist(dto.med_id)
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
    except Exception as e:
        await db_session.rollback()
        raise e

