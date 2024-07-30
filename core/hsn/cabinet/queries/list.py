from typing import List
from shared.db.db_session import session
from shared.db.models.cabinet import CabinetDBModel
from sqlalchemy import select, desc, func
from core.hsn.cabinet.schemas import Cabinet


async def hsn_query_cabinet_list(
    limit: int = None, offset: int = None, pattern: str = None
):
    query = select(CabinetDBModel)

    if hasattr(CabinetDBModel, "is_deleted"):
        query = query.where(CabinetDBModel.is_deleted.is_(False))

    if pattern is not None:
        query = query.where(CabinetDBModel.name.contains(pattern))

    if offset is not None:
        query = query.offset(offset)

    if limit is not None:
        query = query.limit(limit)

    cursor = await session.execute(query)

    return [Cabinet.model_validate(cabinet) for cabinet in cursor.scalars().all()]
