from .router import admin_clinical_assesment_router
from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel
from core.hsn.clinical_assesment import ClinicalAssesment
from api.exceptions import ExceptionResponseSchema, NotFoundException


@admin_clinical_assesment_router.get(
    "/clinical_assesment/{clinical_assesment_id}",
    response_model=ClinicalAssesment,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_clinical_assesment_by_id(clinical_assesment_id: int):
    query = (
        select(ClinicalAssesmentDBModel)
        .where(ClinicalAssesmentDBModel.id == clinical_assesment_id, ClinicalAssesmentDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    clinical_assesment = cursor.scalars().first()
    if clinical_assesment is None:
        raise NotFoundException(message="не найдено!")
    return ClinicalAssesment.model_validate(clinical_assesment)