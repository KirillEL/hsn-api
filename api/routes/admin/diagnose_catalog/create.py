from typing import Optional

from sqlalchemy import select, insert
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema
from shared.db.models.diagnoses_catalog import DiagnosesCatalogDBModel
from .router import admin_diagnose_catalog_router
from core.hsn.diagnoses_catalog import DiagnosesCatalog
from pydantic import BaseModel, Field
from fastapi import Request


class DiagnoseCatalogCreateDto(BaseModel):
    name: str = Field(max_length=255)
    note: Optional[str] = Field(None)


@admin_diagnose_catalog_router.post(
    "/diagnoses_catalog",
    response_model=DiagnosesCatalog,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_diagnose_catalog_create(request: Request, dto: DiagnoseCatalogCreateDto):
    query = (
        insert(DiagnosesCatalogDBModel)
        .values(
            **dto.dict(),
            author_id=request.user.id
        )
        .returning(DiagnosesCatalogDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_diagnose_catalog = cursor.scalars().first()

    return DiagnosesCatalog.model_validate(new_diagnose_catalog)
