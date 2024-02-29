from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from api.exceptions import ExceptionResponseSchema, NotFoundException
from shared.db.models.diagnoses_catalog import DiagnosesCatalogDBModel
from .router import admin_diagnose_catalog_router
from core.hsn.diagnoses_catalog import DiagnosesCatalog


@admin_diagnose_catalog_router.get(
    "/diagnose_catalog/{diagnose_catalog_id}",
    response_model=bool,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_diagnose_catalog_by_id(diagnose_catalog_id: int):
    query = (
        select(DiagnosesCatalogDBModel)
        .where(DiagnosesCatalogDBModel.id == diagnose_catalog_id, DiagnosesCatalogDBModel.is_deleted.is_(False))
    )

    cursor = await db_session.execute(query)
    diagnose_catalog = cursor.scalars().first()
    if diagnose_catalog is None:
        raise NotFoundException(message="не найден!")
    return DiagnosesCatalog.model_validate(diagnose_catalog)