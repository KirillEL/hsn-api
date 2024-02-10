from fastapi import Request, Response
from .router import med_org_router
from typing import List
from api.exceptions import ExceptionResponseSchema
from core.hsn.med_organization import MedOrganization, hsn_query_med_organization_list


@med_org_router.get(
    "",
    response_model=List[MedOrganization],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_med_organization_list(limit: int = None, offset: int = None, pattern: str = None):
    return await hsn_query_med_organization_list(limit, offset, pattern)
