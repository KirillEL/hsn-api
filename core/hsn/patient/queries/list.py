from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel
from core.hsn.patient.model import Patient
from sqlalchemy import select
from api.exceptions import NotFoundException
from sqlalchemy.orm import joinedload


@SessionContext()
async def hsn_patient_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.contragent))
    )

    if hasattr(PatientDBModel, "is_deleted"):
        query = query.where(PatientDBModel.is_deleted.is_(False))

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(PatientDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    await db_session.commit()

    return [Patient.model_validate(patient) for patient in cursor.scalars().all()]
