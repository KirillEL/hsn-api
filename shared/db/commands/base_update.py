from typing import Type
from sqlalchemy import update, select
from ..types import DBModelType
from shared.db.db_session import db_session


async def db_base_entity_update(db_model: Type[DBModelType], entity_id: int, user_id: int, params: dict) -> DBModelType:
    payload = params
    payload['editor_id'] = user_id

    query = update(db_model).where(db_model.id == entity_id) \
        .values(**payload)

    await db_session.execute(query)
    await db_session.commit()

    query = select(db_model).where(db_model.id == entity_id)

    if hasattr(db_model, 'is_deleted'):
        query = query.where(db_model.is_deleted.is_(False))

    cursor = await db_session.execute(query)
    result = cursor.first()

    return None if result[0] is None else result[0]
