from .router import cabinet_router
from fastapi import Request, Response
from core.hsn.cabinet.model import Cabinet
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from typing import Optional
from core.hsn.cabinet import HsnCabinetUpdateContext, hsn_cabinet_update


class CabinetUpdateRequest(BaseModel):
    name: str = Field(..., description="The name of the cabinet", max_length=100)
    med_id: Optional[int] = Field(None, gt=0)


@cabinet_router.put(
    "/{cabinet_id}",
    response_model=Cabinet,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_cabinet_update(cabinet_id: int, request: Request, req_body: CabinetUpdateRequest):
    context = HsnCabinetUpdateContext(id=cabinet_id, med_id=req_body.med_id, name=req_body.name,
                                      user_id=request.user.id)
    return await hsn_cabinet_update(context)
