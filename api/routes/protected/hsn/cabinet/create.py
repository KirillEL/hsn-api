from pydantic import BaseModel, Field
from fastapi import Request
from .router import cabinet_router
from api.exceptions import ExceptionResponseSchema, BadRequestException
from core.hsn.cabinet.model import Cabinet
from core.hsn.cabinet import HsnCabinetCreateContext, hsn_cabinet_create


class CabinetCreateRequest(BaseModel):
    number: str = Field(..., max_length=200)
    med_id: int = Field(..., gt=0)


@cabinet_router.post(
    "",
    response_model=Cabinet,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Create a Cabinet"
)
async def api_hsn_cabinet_create(request: Request, body: CabinetCreateRequest):
    params = HsnCabinetCreateContext(user_id=request.user.id, number=body.number, med_id=body.med_id)

    new_cabinet = await hsn_cabinet_create(params)
    if new_cabinet is None:
        raise BadRequestException
    return new_cabinet
