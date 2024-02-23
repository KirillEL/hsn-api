from fastapi import Request

from api.decorators import admin_required
from .router import cabinet_router
from pydantic import BaseModel, Field
from core.hsn.cabinet import Cabinet
from typing import List
from api.exceptions import ExceptionResponseSchema
from core.hsn.cabinet import hsn_query_cabinet_list


@cabinet_router.get(
    "/get/all",
    response_model=List[Cabinet],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@admin_required
async def api_hsn_cabinet_list(request: Request, limit: int = None, offset: int = None, pattern: str = None):
    return await hsn_query_cabinet_list(limit, offset, pattern)
