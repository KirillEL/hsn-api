from sqlalchemy import select

from api.decorators import HandleExceptions
from shared.db.models.med_organization import MedOrganizationDBModel
from shared.db.db_session import session
from core.hsn.med_organization import MedOrganization


async def hsn_query_med_organization_list(limit: int = None, offset: int = None, pattern: str = None):
    query = select(MedOrganizationDBModel)

    if hasattr(MedOrganizationDBModel, 'is_deleted'):
        query = query.where(MedOrganizationDBModel.is_deleted.is_(False))

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(MedOrganizationDBModel.name.contains(pattern))

    cursor = await session.execute(query)
    return [MedOrganization.model_validate(item) for item in cursor.scalars().all()]
