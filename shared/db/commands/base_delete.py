from typing import Type
from sqlalchemy import update
from shared.db.db_session import session
from ..types import DBModelType


async def db_base_entity_delete(db_model: Type[DBModelType], entity_id: int, user_id: int) -> None:
    payload = {
        'deleter_id': user_id,
        'is_deleted': True
    }

    query = update(db_model).where(db_model.id == entity_id) \
        .values(**payload)

    await session.execute(query)
    return None
