from sqlalchemy import update
from shared.db.db_session import db_session, SessionContext
from shared.db.models.cabinet import CabinetDBModel
from core.hsn.cabinet import Cabinet
from .router import admin_cabinet_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@admin_cabinet_router.delete(
    "/cabinets/{cabinet_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_cabinet_delete(cabinet_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }

    query = (
        update(CabinetDBModel)
        .values(**payload)
        .where(CabinetDBModel.id == cabinet_id)
    )
    await db_session.execute(query)
    await db_session.commit()

    return True

