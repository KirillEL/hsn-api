from shared.db.db_session import SessionContext, db_session
from pydantic import BaseModel, Field
from typing import Optional
from shared.db.commands import db_base_entity_update
from shared.db.models import CabinetDBModel
from core.hsn.cabinet.model import Cabinet


class HsnCabinetUpdateContext(BaseModel):
    user_id: int = Field(None, gt=0)
    id: int = Field(None, gt=0)
    number: str
    med_id: Optional[int] = Field(None, gt=0)


@SessionContext()
async def hsn_cabinet_update(context: HsnCabinetUpdateContext):
    payload = context.model_dump(exclude={'user_id'})
    entity_db = await db_base_entity_update(db_model=CabinetDBModel, entity_id=context.id, user_id=context.user_id,
                                            params=payload)
    return Cabinet.model_validate(entity_db)
