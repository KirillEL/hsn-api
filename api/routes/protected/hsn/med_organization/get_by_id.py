from .router import med_org_router
from fastapi import Request, Response
from core.hsn.med_organization import MedOrganization
from api.exceptions import ExceptionResponseSchema


@med_org_router.get(
    "/{med_id}",
    response_model=MedOrganization | None,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_med_organization_get_by_id(med_id: int):
    pass
