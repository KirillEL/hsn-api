from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_group import MedicinesGroupDBModel
from .router import admin_medicine_group_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.medicines_group import MedicinesGroup


@admin_medicine_group_router.get(
    "/medicine_groups",
    response_model=list[MedicinesGroup],
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_group_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(MedicinesGroupDBModel)
        .where(MedicinesGroupDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(MedicinesGroupDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    medicine_groups = cursor.scalars().all()

    return [MedicinesGroup.model_validate(m) for m in medicine_groups]
