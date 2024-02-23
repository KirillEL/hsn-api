from fastapi import Request, Response

from api.decorators import admin_required
from .router import med_org_router
from core.hsn.med_organization import MedOrganizationFlat, MedOrganization
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from core.hsn.med_organization import UpdateMedOrganizationContext, hsn_med_organization_update


class MedOrganizationUpdateResponse(BaseModel):
    name: str


class MedOrganizationUpdateRequest(BaseModel):
    name: str = Field(..., description="новое имя организации", max_length=100)
    number: int = Field(...)
    address: str = Field(None, max_length=1000)


@med_org_router.put(
    "/{med_id}",
    response_model=MedOrganization,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@admin_required
async def api_med_organization_update(med_id: int, request: Request, req_body: MedOrganizationUpdateRequest):
    context = UpdateMedOrganizationContext(user_id=request.user.id, id=med_id,
                                           name=req_body.name,
                                           number=req_body.number,
                                           address=req_body.address)
    return await hsn_med_organization_update(context)

