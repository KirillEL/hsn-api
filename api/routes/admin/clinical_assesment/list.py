from .router import admin_clinical_assesment_router
from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel
from core.hsn.clinical_assesment import ClinicalAssesment
from api.exceptions import ExceptionResponseSchema


@admin_clinical_assesment_router.get(
    "/clinical_assesments",
    response_model=list[ClinicalAssesment],
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_clinical_assesments_list(limit: int = None, offset: int = None):
    query = (
        select(ClinicalAssesmentDBModel)
        .where(ClinicalAssesmentDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    cursor = await db_session.execute(query)
    clinical_assesments = cursor.scalars().all()

    return [ClinicalAssesment.model_validate(ca) for ca in clinical_assesments]

