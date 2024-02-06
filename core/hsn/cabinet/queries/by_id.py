from typing import Optional
from shared.db.db_session import SessionContext, db_session
from shared.db.models.cabinet import CabinetDBModel
from sqlalchemy import select


@SessionContext()
async def hsn_query_cabinet_by_id(cabinet_id: int):
    query = select([CabinetDBModel]).where(CabinetDBModel.id == cabinet_id)

    if hasattr(CabinetDBModel, 'is_deleted'):
        query = query.where(CabinetDBModel.is_deleted.is_(False))

    cursor = await db_session.execute(query)
    result = cursor.first()

    return None if result is None else result[CabinetDBModel]


