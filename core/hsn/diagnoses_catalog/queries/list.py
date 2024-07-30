from sqlalchemy import select
from shared.db.models.diagnoses_catalog import DiagnosesCatalogDBModel
from shared.db.db_session import db_session, SessionContext
from sqlalchemy.sql.expression import func

# add validation in return


@SessionContext()
async def hsn_query_diagnoses_catalog_list(
    limit: int = None, offset: int = None, pattern: str = None
):
    query = select([DiagnosesCatalogDBModel])

    if hasattr(DiagnosesCatalogDBModel, "is_deleted"):
        query = query.where(DiagnosesCatalogDBModel.is_deleted.is_(False))

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(func.ilike(DiagnosesCatalogDBModel, f"%{pattern}%"))

    cursor = await db_session.execute(query)

    return [item for item in cursor.all()]
