from fastapi import Request, Response
from .router import med_org_router
from core.hsn.med_organization import MedOrganizationFlat, MedOrganization
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from core.hsn.med_organization import UpdateMedOrganizationContext, hsn_med_organization_update


class MedOrganizationUpdateResponse(BaseModel):
    name: str


class MedOrganizationUpdateRequest(BaseModel):
    name: str = Field(..., description="новое имя организации", max_length=100)


@med_org_router.put(
    "/{med_id}",
    response_model=MedOrganization,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_med_organization_update(med_id: int, request: Request, req_body: MedOrganizationUpdateRequest):
    context = UpdateMedOrganizationContext(user_id=request.user.id, id=med_id, name=req_body.name)
    return await hsn_med_organization_update(context)

