from .router import cabinet_router
from fastapi import Request, Response
from core.hsn.cabinet import Cabinet
from api.exceptions import ExceptionResponseSchema
from core.hsn.cabinet import hsn_query_cabinet_by_id
from api.exceptions import NotFoundException


@cabinet_router.get(
    "/{cabinet_id}",
    response_model=Cabinet,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_cabinet_get_by_id(cabinet_id: int):
    cabinet = await hsn_query_cabinet_by_id(cabinet_id)
    if cabinet is None:
        raise NotFoundException(message="cabinet not found!")
    return cabinet
