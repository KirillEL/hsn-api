from api.decorators import HandleExceptions
from shared.db import Transaction
from shared.db.models.med_organization import MedOrganizationDBModel
from pydantic import BaseModel, Field
from shared.db.commands import db_base_entity_update
from core.hsn.med_organization import MedOrganization, MedOrganizationFlat
from shared.db.transaction import Propagation


class UpdateMedOrganizationContext(BaseModel):
    user_id: int = Field(None, gt=0)
    id: int = Field(None, gt=0)
    name: str = Field(None, max_length=100)
    number: int = Field(None, gt=0)
    address: str = Field(None, max_length=1000)


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_med_organization_update(context: UpdateMedOrganizationContext):
    payload = context.model_dump(exclude={'user_id'})
    entity_db = await db_base_entity_update(db_model=MedOrganizationDBModel, entity_id=context.id,
                                            user_id=context.user_id, params=payload)
    return MedOrganization.model_validate(entity_db)
