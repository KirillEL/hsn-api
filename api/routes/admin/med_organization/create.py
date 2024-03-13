from sqlalchemy import insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.med_organization import MedOrganizationDBModel
from core.hsn.med_organization import MedOrganization
from .router import admin_med_org_router
from api.exceptions import ExceptionResponseSchema, ValidationException
from pydantic import BaseModel, Field, ValidationError
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
    try:
        query = (
            insert(MedOrganizationDBModel)
            .values(
                **dto.dict(),
                author_id=request.user.id
            )
            .returning(MedOrganizationDBModel)
        )

        cursor = await db_session.execute(query)

        new_med_org = cursor.scalars().first()
        validated_med_org = MedOrganization.model_validate(new_med_org)
        await db_session.commit()
        return validated_med_org
    except ValidationError as ve:
        raise ValidationException(message=str(ve))
    except Exception as ex:
        await db_session.rollback()
        raise ex
