from fastapi import Request
from .router import cabinet_router
from pydantic import BaseModel, Field
from core.hsn.cabinet import Cabinet
from typing import List
from api.exceptions import ExceptionResponseSchema



@cabinet_router.get(
    "/",
    response_model=List[Cabinet],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def api_hsn_cabinet_list(request: Request):
    pass
    

