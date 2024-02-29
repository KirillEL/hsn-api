from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.med_organization import MedOrganizationDBModel
from core.hsn.med_organization import MedOrganization
from .router import admin_med_org_router
from api.exceptions import ExceptionResponseSchema, NotFoundException


@admin_med_org_router.get(
    "/med_organization/{med_organization_id}",
    response_model=MedOrganization,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_med_org_by_id(med_organization_id: int):
    query = (
        select(MedOrganizationDBModel)
        .where(MedOrganizationDBModel.id == med_organization_id, MedOrganizationDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    med_org = cursor.scalars().first()
    if med_org is None:
        raise NotFoundException(message="Организация не найдена!")
    return MedOrganization.model_validate(med_org)