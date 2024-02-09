from pydantic import BaseModel
from fastapi import Request
from .router import cabinet_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.cabinet.model import Cabinet
from core.hsn.cabinet import HsnCabinetCreateContext, hsn_cabinet_create


class CabinetCreateResponse(Cabinet):
    pass


class CabinetCreateRequest(BaseModel):
    name: str
    med_id: int


@cabinet_router.post(
    "",
    response_model=CabinetCreateResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_hsn_cabinet_create(request: Request, body: CabinetCreateRequest):
    params = HsnCabinetCreateContext(user_id=request.user.id, name=body.name, med_id=body.med_id)
    return await hsn_cabinet_create(params)

