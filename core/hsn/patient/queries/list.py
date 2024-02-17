from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel
from core.hsn.patient.model import Patient
from sqlalchemy import select
from api.exceptions import NotFoundException


@SessionContext()
async def hsn_patient_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(PatientDBModel)
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(PatientDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    await db_session.commit()

    return [Patient.model_validate(item[0]) for item in cursor.all()]
