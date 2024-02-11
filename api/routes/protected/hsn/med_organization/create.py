from fastapi import Request, Response
from .router import med_org_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.med_organization import MedOrganization
from pydantic import BaseModel, Field
from shared.db.models.med_organization import MedOrganizationDBModel
from core.hsn.med_organization import hsn_med_organization_create, CreateMedOrganizationContext
from core.user import UserAuthor


class MedOrganizationCreateResponse(BaseModel):
    name: str
    created_by: UserAuthor


class MedOrganizationCreateRequest(BaseModel):
    name: str = Field(..., description="Название мед организации", max_length=100)


@med_org_router.post(
    "",
    response_model=MedOrganizationCreateResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_med_organization_create(request: Request, req_body: MedOrganizationCreateRequest):
    context = CreateMedOrganizationContext(user_id=request.user.id, name=req_body.name)
    return await hsn_med_organization_create(context)

