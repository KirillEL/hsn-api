from fastapi import Request, Response
from .router import cabinet_router
from pydantic import BaseModel
from api.exceptions import ExceptionResponseSchema
from core.hsn.cabinet import hsn_cabinet_delete, CabinetDeleteContext


@cabinet_router.delete(
    "/{cabinet_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_cabinet_delete(cabinet_id: int, request: Request):
    context = CabinetDeleteContext(user_id=request.user.id, id=cabinet_id)
    await hsn_cabinet_delete(context)
    return True
