from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema
from shared.db.models.diagnoses_catalog import DiagnosesCatalogDBModel
from .router import admin_diagnose_catalog_router
from core.hsn.diagnoses_catalog import DiagnosesCatalog
from pydantic import BaseModel, Field
from fastapi import Request
from sqlalchemy import update


@admin_diagnose_catalog_router.delete(
    "/diagnoses_catalog/{diagnose_catalog_id}",
    response_model=bool,
    responses={'400': {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_diagnose_catalog_delete(diagnose_catalog_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_by': request.user.id
    }
    query = (
        update(DiagnosesCatalogDBModel)
        .values(**payload)
        .where(DiagnosesCatalogDBModel.id == diagnose_catalog_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True
