from shared.db.db_session import db_session, SessionContext
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel
from sqlalchemy import delete


@SessionContext()
async def hsn_clinical_assesment_delete(clinical_assesment_id: int):
    """Delete clinical assesment"""
    query = (
        delete(ClinicalAssesmentDBModel)
        .where(ClinicalAssesmentDBModel.id == clinical_assesment_id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    return None
