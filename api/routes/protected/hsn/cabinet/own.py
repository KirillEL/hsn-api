from .router import cabinet_router
from core.hsn.cabinet import Cabinet
from api.exceptions import ExceptionResponseSchema
from fastapi import Request
from core.hsn.cabinet import hsn_cabinet_own
from core.user import hsn_user_get_me

@cabinet_router.get(
    "/get/own",
    response_model=Cabinet,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Получить свой кабинет"
)
async def api_cabinet_own(request: Request):
    user = await hsn_user_get_me(request.user.id)
    return await hsn_cabinet_own(user.doctor.id)
