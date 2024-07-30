from typing import Type
from sqlalchemy import update, select

from .. import Transaction
from ..transaction import Propagation
from ..types import DBModelType
from shared.db.db_session import session


async def db_base_entity_update(
    db_model: Type[DBModelType], entity_id: int, user_id: int, params: dict
) -> DBModelType:
    payload = params
    payload["editor_id"] = user_id

    query = update(db_model).where(db_model.id == entity_id).values(**payload)

    await session.execute(query)

    query = select(db_model).where(db_model.id == entity_id)

    if hasattr(db_model, "is_deleted"):
        query = query.where(db_model.is_deleted.is_(False))

    cursor = await session.execute(query)
    result = cursor.first()

    return None if result[0] is None else result[0]
