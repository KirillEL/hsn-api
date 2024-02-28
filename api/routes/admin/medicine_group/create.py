from typing import Optional

from sqlalchemy import select, insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_group import MedicinesGroupDBModel
from .router import admin_medicine_group_router
from api.exceptions import ExceptionResponseSchema
from core.hsn.medicines_group import MedicinesGroup
from pydantic import BaseModel, Field
from fastapi import Request


class MedicinesGroupCreateDto(BaseModel):
    name: str = Field(max_length=255)
    code: str = Field(max_length=50)
    note: Optional[str] = Field(None)


@admin_medicine_group_router.post(
    "/medicine_groups",
    response_model=MedicinesGroup,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_group_create(request: Request, dto: MedicinesGroupCreateDto):
    query = (
        insert(MedicinesGroupDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(MedicinesGroupDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_medicine_group = cursor.scalars().first()

    return MedicinesGroup.model_validate(new_medicine_group)
