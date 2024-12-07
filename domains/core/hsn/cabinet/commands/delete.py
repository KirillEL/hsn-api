from domains.shared.db.db_session import SessionContext
from pydantic import BaseModel, Field
from domains.shared.db.commands import db_base_entity_delete
from domains.shared.db.models import CabinetDBModel


class CabinetDeleteContext(BaseModel):
    user_id: int = Field(None, gt=0)
    id: int = Field(None, gt=0)


@SessionContext()
async def hsn_cabinet_delete(context: CabinetDeleteContext):
    return await db_base_entity_delete(
        db_model=CabinetDBModel, entity_id=context.id, user_id=context.user_id
    )
