from typing import Type
from sqlalchemy import select
from shared.db.db_session import db_session
from shared.db.types import DBModelType


async def db_query_entity_by_id(db_model: Type[DBModelType], entity_id: int) -> Type[DBModelType]:
    query = (
        select(db_model)
        .where(db_model.id == entity_id)
    )

    if hasattr(db_model, 'is_deleted'):
        query = query.where(db_model.is_deleted.is_(False))

    cursor = await db_session.execute(query)
    model = cursor.scalars().first()

    return None if model is None else model
