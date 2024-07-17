from core.hsn.cabinet import hsn_query_cabinet_list
from core.hsn.cabinet.schemas import CabinetFlatResponse
from .router import cabinet_router
from api.exceptions import ExceptionResponseSchema


@cabinet_router.get(
    "",
    response_model=list[CabinetFlatResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Получить список доступных кабинетов"
)
async def get_cabinets(limit: int = None, offset: int = None, pattern: str = None):
    return await hsn_query_cabinet_list(limit, offset, pattern)
