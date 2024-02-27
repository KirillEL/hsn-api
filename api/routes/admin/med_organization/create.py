from sqlalchemy import insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.med_organization import MedOrganizationDBModel
from core.hsn.med_organization import MedOrganization
from .router import admin_med_org_router
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from fastapi import Request


class CreateMedOrganizationDto(BaseModel):
    name: str
    number: int
    address: str


@admin_med_org_router.post(
    "/med_organizations",
    response_model=MedOrganization,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_med_organization_create(request: Request, dto: CreateMedOrganizationDto):
    query = (
        insert(MedOrganizationDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(MedOrganizationDBModel)
    )

    cursor = await db_session.execute(query)
    new_med_org = cursor.scalars().first()

    return MedOrganization.model_validate(new_med_org)