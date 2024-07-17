from typing import Optional
from shared.db.db_session import session
from shared.db.models.cabinet import CabinetDBModel
from sqlalchemy import select
from core.hsn.cabinet.schemas import CabinetFlat, Cabinet
from typing import Optional
from api.exceptions import NotFoundException


async def hsn_query_cabinet_by_id(cabinet_id: int) -> Optional[Cabinet]:
    query = (
        select(CabinetDBModel)
        .where(CabinetDBModel.id == cabinet_id)
    )

    if hasattr(CabinetDBModel, "is_deleted"):
        query = query.where(CabinetDBModel.is_deleted.is_(False))

    cursor = await session.execute(query)
    cabinet = cursor.first()
    if cabinet is None:
        raise NotFoundException(message="кабинет не найден!")
    return Cabinet.model_validate(cabinet[0])



