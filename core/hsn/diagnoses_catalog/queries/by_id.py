from sqlalchemy import select
from shared.db.models.diagnoses_catalog import DiagnosesCatalogDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_query_diagneses_catalog_by_id(diagnoses_id: int):
    query = select([DiagnosesCatalogDBModel])

    if hasattr(DiagnosesCatalogDBModel, 'is_deleted'):
        query = query.where(DiagnosesCatalogDBModel.is_deleted.is_(False))

    query = query.where(DiagnosesCatalogDBModel.id == diagnoses_id)

    cursor = await db_session.execute(query)
    result = cursor.first()
    return None if result is None else result[DiagnosesCatalogDBModel]

