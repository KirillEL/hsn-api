from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema
from .router import admin_cabinet_router
from core.hsn.cabinet import Cabinet
from shared.db.models.cabinet import CabinetDBModel


@admin_cabinet_router.get(
    "/cabinets/{cabinet_id}",
    response_model=Cabinet,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_cabinet_by_id(cabinet_id: int):
    query = (
        select(CabinetDBModel)
        .where(CabinetDBModel.cabinet_id == cabinet_id, CabinetDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    cabinet = cursor.scalars().first()

    return Cabinet.model_validate(cabinet)