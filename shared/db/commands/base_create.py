from typing import Type

from .. import session
from ..types import DBModelType


async def db_base_entity_create(
    db_model: Type[DBModelType], user_id: int, params: dict
) -> DBModelType:
    payload = params
    payload["author_id"] = user_id
    model = db_model(**payload)

    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model
