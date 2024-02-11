from .router import med_org_router
from fastapi import Request, Response
from core.hsn.med_organization import MedOrganization
from api.exceptions import ExceptionResponseSchema
from api.exceptions import NotFoundException
from core.hsn.med_organization import hsn_query_med_organization_by_id
from pydantic import BaseModel
from core.user import UserAuthor

class MedOrganizationGetByIdResponse(BaseModel):
    id: int
    name: str
    created_by: UserAuthor

@med_org_router.get(
    "/{med_id}",
    response_model=MedOrganizationGetByIdResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_med_organization_get_by_id(med_id: int):
    med_org = await hsn_query_med_organization_by_id(med_id)
    if med_org is None:
        raise NotFoundException(message="мед учреждение не найдено!")
    return med_org
