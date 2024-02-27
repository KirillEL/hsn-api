from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.med_organization import MedOrganizationDBModel
from core.hsn.med_organization import MedOrganization
from .router import admin_med_org_router
from api.exceptions import ExceptionResponseSchema


@admin_med_org_router.get(
    "/med_organizations",
    response_model=list[MedOrganization],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_med_org_list():
    query = (
        select(MedOrganizationDBModel)
        .where(MedOrganizationDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    med_orgs = cursor.scalars().all()

    return [MedOrganization.model_validate(med) for med in med_orgs]
