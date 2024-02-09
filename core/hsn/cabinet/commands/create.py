from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from ..model import Cabinet
from sqlalchemy import insert
from shared.db.models.cabinet import CabinetDBModel
from shared.db.commands import db_base_entity_create


class HsnCabinetCreateContext(BaseModel):
    user_id: int = Field(..., gt=0)
    name: str = Field(..., max_length=150)
    # add med_id
    med_id: int = Field(gt=0)


@SessionContext()
async def hsn_cabinet_create(context: HsnCabinetCreateContext) -> Cabinet:
    payload = context.model_dump(exclude={'user_id'})
    entity_db = await db_base_entity_create(CabinetDBModel, context.user_id, payload)
    return Cabinet.model_validate(entity_db)



