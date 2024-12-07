from sqlalchemy import select

from domains.shared.db.models.med_organization import MedOrganizationDBModel
from domains.shared.db.db_session import db_session, SessionContext
from domains.core.hsn.med_organization import MedOrganization
from api.exceptions import NotFoundException


@SessionContext()
async def hsn_query_med_organization_by_id(med_organization_id: int):
    query = select(MedOrganizationDBModel).where(
        MedOrganizationDBModel.id == med_organization_id
    )

    if hasattr(MedOrganizationDBModel, "is_deleted"):
        query = query.where(MedOrganizationDBModel.is_deleted.is_(False))

    cursor = await db_session.execute(query)
    med_organization = cursor.scalars().first()
    if not med_organization:
        raise NotFoundException(
            message=f"Мед учреждение с id: {med_organization_id} не найдено"
        )
    return MedOrganization.model_validate(med_organization)
