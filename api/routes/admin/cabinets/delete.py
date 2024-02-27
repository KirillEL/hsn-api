from sqlalchemy import delete
from shared.db.db_session import db_session, SessionContext
from shared.db.models.cabinet import CabinetDBModel
from core.hsn.cabinet import Cabinet
from .router import admin_cabinet_router
from api.exceptions import ExceptionResponseSchema


@admin_cabinet_router.delete(
    "/cabinets/{cabinet_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_cabinet_delete(cabinet_id: int):
    query = (
        delete(CabinetDBModel)
        .where(CabinetDBModel.id == cabinet_id)
    )
    await db_session.execute(query)
    return True

