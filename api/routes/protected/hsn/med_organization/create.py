from fastapi import Request, Response

from api.decorators import admin_required
from .router import med_org_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.med_organization import MedOrganization
from pydantic import BaseModel, Field
from shared.db.models.med_organization import MedOrganizationDBModel
from core.hsn.med_organization import hsn_med_organization_create, CreateMedOrganizationContext
from core.user import UserAuthor


class MedOrganizationCreateResponse(BaseModel):
    id: int
    name: str
    number: int
    address: str
    created_by: UserAuthor


class MedOrganizationCreateRequest(BaseModel):
    name: str = Field(..., description="Название мед организации", max_length=100)
    number: int = Field(..., description="Номер")
    address: str = Field(..., description="адресс", max_length=1000)


@med_org_router.post(
    "",
    response_model=MedOrganizationCreateResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@admin_required
async def api_med_organization_create(request: Request, req_body: MedOrganizationCreateRequest):
    context = CreateMedOrganizationContext(
        user_id=request.user.id,
        name=req_body.name,
        number=req_body.number,
        address=req_body.address
    )
    return await hsn_med_organization_create(context)

