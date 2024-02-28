from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema
from shared.db.models.diagnoses_catalog import DiagnosesCatalogDBModel
from .router import admin_diagnose_catalog_router
from core.hsn.diagnoses_catalog import DiagnosesCatalog
from pydantic import BaseModel, Field
from fastapi import Request
from sqlalchemy import update, select


@admin_diagnose_catalog_router.get(
    "/diagnoses_catalog",
    response_model=list[DiagnosesCatalog],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_diagnose_catalog_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(DiagnosesCatalogDBModel)
        .where(DiagnosesCatalogDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(DiagnosesCatalogDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    diagnose_catalogs = cursor.scalars().all()

    return [DiagnosesCatalog.model_validate(d_c) for d_c in diagnose_catalogs]
