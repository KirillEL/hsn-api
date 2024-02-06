from .router import user_router
from api.exceptions import ExceptionResponseSchema
from fastapi import Request

from .schemas import UserResponse


@user_router.get(
    "/me",
    response_model=UserResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_current_user(req: Request):
    pass