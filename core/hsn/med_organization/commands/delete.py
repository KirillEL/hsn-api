from shared.db.commands import db_base_entity_delete
from shared.db.db_session import SessionContext
from pydantic import BaseModel, Field
from shared.db.models.med_organization import MedOrganizationDBModel


class DeleteMedOrganizationContext(BaseModel):
    user_id: int = Field(None, gt=0)
    id: int = Field(None, gt=0)


@SessionContext()
async def hsn_med_organization_delete(context: DeleteMedOrganizationContext):
    return await db_base_entity_delete(MedOrganizationDBModel, entity_id=context.id, user_id=context.user_id)
