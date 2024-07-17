from shared.db import Transaction
from shared.db.transaction import Propagation
from ..schemas import MedOrganizationFlat, MedOrganization
from shared.db.commands import db_base_entity_create
from pydantic import BaseModel, Field
from shared.db.models.med_organization import MedOrganizationDBModel


class CreateMedOrganizationContext(BaseModel):
    user_id: int = Field(None, gt=0)
    name: str = Field(None, max_length=100)
    number: int = Field(None, gt=0)
    address: str = Field(None, max_length=1000)

@Transaction(propagation=Propagation.REQUIRED)
async def hsn_med_organization_create(context: CreateMedOrganizationContext):
    payload = context.model_dump(exclude={'user_id'})
    entity_db = await db_base_entity_create(db_model=MedOrganizationDBModel, user_id=context.user_id, params=payload)
    return MedOrganization.model_validate(entity_db)
