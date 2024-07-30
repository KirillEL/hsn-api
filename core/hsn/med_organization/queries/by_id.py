from sqlalchemy import select

from api.decorators import HandleExceptions
from shared.db.models.med_organization import MedOrganizationDBModel
from shared.db.db_session import session
from core.hsn.med_organization import MedOrganization
from api.exceptions import NotFoundException


async def hsn_query_med_organization_by_id(med_organization_id: int):
    query = select(MedOrganizationDBModel).where(
        MedOrganizationDBModel.id == med_organization_id
    )

    if hasattr(MedOrganizationDBModel, "is_deleted"):
        query = query.where(MedOrganizationDBModel.is_deleted.is_(False))

    cursor = await session.execute(query)
    med_organization = cursor.scalars().first()
    if not med_organization:
        raise NotFoundException(message="не найдено!")
    return MedOrganization.model_validate(med_organization)
