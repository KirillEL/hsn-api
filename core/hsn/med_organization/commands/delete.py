from api.decorators import HandleExceptions
from shared.db import Transaction
from shared.db.commands import db_base_entity_delete
from pydantic import BaseModel, Field
from shared.db.models.med_organization import MedOrganizationDBModel
from shared.db.transaction import Propagation


class DeleteMedOrganizationContext(BaseModel):
    user_id: int = Field(None, gt=0)
    id: int = Field(None, gt=0)


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_med_organization_delete(context: DeleteMedOrganizationContext):
    return await db_base_entity_delete(
        MedOrganizationDBModel, entity_id=context.id, user_id=context.user_id
    )
