from typing import Type
from shared.db.db_session import db_session
from ..types import DBModelType


async def db_base_entity_create(
    db_model: Type[DBModelType], user_id: int, params: dict
) -> DBModelType:
    payload = params
    payload["author_id"] = user_id
    model = db_model(**payload)

    db_session.add(model)
    await db_session.commit()
    await db_session.refresh(model)
    return model
