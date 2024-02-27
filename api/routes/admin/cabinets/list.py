from .router import admin_cabinet_router
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from core.hsn.cabinet import Cabinet
from api.exceptions import ExceptionResponseSchema
from shared.db.models.cabinet import CabinetDBModel


@admin_cabinet_router.get(
    "/cabinets",
    response_model=list[Cabinet],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_cabinets_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(CabinetDBModel)
        .where(CabinetDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(CabinetDBModel.number.contains(pattern))

    cursor = await db_session.execute(query)
    cabinets = cursor.scalars().all()

    return [Cabinet.model_validate(cabinet) for cabinet in cabinets]
