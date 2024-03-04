from .router import admin_clinical_assesment_router
from sqlalchemy import select, insert, update
from shared.db.db_session import db_session, SessionContext
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@admin_clinical_assesment_router.delete(
    "/clinical_assesments/{clinical_assessment_id}",
    response_model=bool,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_clinical_assesment_delete(clinical_assessment_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }

    query = (
        update(ClinicalAssesmentDBModel)
        .values(**payload)
        .where(ClinicalAssesmentDBModel.id == clinical_assessment_id)
    )

    await db_session.execute(query)
    await db_session.commit()

    return True
