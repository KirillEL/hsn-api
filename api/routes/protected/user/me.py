from core.user.queries.by_id import user_query_by_id
from .router import user_router
from api.exceptions import ExceptionResponseSchema, NotFoundException
from fastapi import Request

from .schemas import UserResponse


@user_router.get(
    "/me",
    response_model=UserResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_current_user(req: Request):
    print(req.user)
    user = await user_query_by_id(req.user.id)
    if user is None:
        raise NotFoundException
    return user