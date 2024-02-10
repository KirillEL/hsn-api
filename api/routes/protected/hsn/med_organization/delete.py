from fastapi import Request, Response
from .router import med_org_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.med_organization import DeleteMedOrganizationContext, hsn_med_organization_delete


@med_org_router.delete(
    "/{med_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_med_organization_delete(med_id: int, request: Request):
    context = DeleteMedOrganizationContext(user_id=request.user.id, med_id=med_id)
    await hsn_med_organization_delete(context)
    return True
