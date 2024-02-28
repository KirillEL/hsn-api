from typing import Optional

from sqlalchemy import select, insert, update
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_group import MedicinesGroupDBModel
from .router import admin_medicine_group_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.medicines_group import MedicinesGroup
from pydantic import BaseModel, Field
from fastapi import Request


@admin_medicine_group_router.delete(
    "/medicine_groups/{medicine_group_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_group_delete(medicine_group_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }

    query = (
        update(MedicinesGroupDBModel)
        .values(**payload)
        .where(MedicinesGroupDBModel.id == medicine_group_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True
