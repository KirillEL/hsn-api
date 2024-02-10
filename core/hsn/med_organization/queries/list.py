from sqlalchemy import select
from shared.db.models.med_organization import MedOrganizationDBModel
from shared.db.db_session import db_session, SessionContext


# TODO: add validation in return

@SessionContext()
async def hsn_query_med_organization_list(limit: int = None, offset: int = None, pattern: str = None):
    query = select([MedOrganizationDBModel])

    if hasattr(MedOrganizationDBModel, 'is_deleted'):
        query = query.where(MedOrganizationDBModel.is_deleted == False)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(MedOrganizationDBModel.name.ilike(f'%{pattern}%'))

    cursor = await db_session.execute(query)

    return [item for item in cursor.all()]
