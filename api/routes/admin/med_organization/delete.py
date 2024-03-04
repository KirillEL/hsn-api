from .router import admin_med_org_router
from fastapi import Request
from shared.db.db_session import db_session, SessionContext
from shared.db.models.med_organization import MedOrganizationDBModel
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import update


@admin_med_org_router.delete(
    "/admin/med_organizations/{med_org_id}",
    response_model=bool,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_med_organization_delete(med_org_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }

    query = (
        update(MedOrganizationDBModel)
        .values(**payload)
        .where(MedOrganizationDBModel.id == med_org_id)
    )

    await db_session.execute(query)
    await db_session.commit()

    return True

