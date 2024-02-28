from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_group import MedicinesGroupDBModel
from .router import admin_medicine_group_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.medicines_group import MedicinesGroup


@admin_medicine_group_router.get(
    "/medicine_groups/{medicine_group_id}",
    response_model=MedicinesGroup,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_group_by_id(medicine_group_id: int):
    query = (
        select(MedicinesGroupDBModel)
        .where(MedicinesGroupDBModel.id == medicine_group_id, MedicinesGroupDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    medicine_group = cursor.scalars().first()

    return MedicinesGroup.model_validate(medicine_group)