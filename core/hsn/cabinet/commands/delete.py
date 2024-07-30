from pydantic import BaseModel, Field

from shared.db import Transaction
from shared.db.commands import db_base_entity_delete
from shared.db.models import CabinetDBModel
from shared.db.transaction import Propagation


class CabinetDeleteContext(BaseModel):
    user_id: int = Field(None, gt=0)
    id: int = Field(None, gt=0)


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_cabinet_delete(context: CabinetDeleteContext):
    return await db_base_entity_delete(
        db_model=CabinetDBModel, entity_id=context.id, user_id=context.user_id
    )
