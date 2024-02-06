from sqlalchemy import select
from shared.db.models.med_organization import MedOrganizationDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_query_med_organization_by_id(med_organization_id: int):
    query = select([MedOrganizationDBModel])

    if hasattr(MedOrganizationDBModel, 'is_deleted'):
        query = query.where(MedOrganizationDBModel.is_deleted.is_(False))

    query = query.where(MedOrganizationDBModel.id == med_organization_id)

    cursor = await db_session.execute(query)
    result = cursor.first()

    return None if result is None else result[MedOrganizationDBModel]
