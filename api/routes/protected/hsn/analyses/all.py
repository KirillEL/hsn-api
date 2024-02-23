from typing import List
from fastapi import Request, Response
from api.decorators import admin_required
from api.exceptions import ExceptionResponseSchema

from .router import analyses_router


@analyses_router.get(
    "/all",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Получить список анализов"
)
@admin_required
async def api_analyses_list(request: Request, limit: int = None, offset: int = None, pattern: str = None):
    pass
