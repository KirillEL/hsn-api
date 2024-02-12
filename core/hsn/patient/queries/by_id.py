from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel
from core.hsn.patient.model import Patient
from sqlalchemy import select
from api.exceptions import NotFoundException


@SessionContext()
async def hsn_patient_by_id(patient_id: int):
    query = (
        select(PatientDBModel)
        .where(PatientDBModel.id == patient_id)
    )

    if hasattr(PatientDBModel, "is_deleted"):
        query = query.where(PatientDBModel.is_deleted.is_(False))

    cursor = await db_session.execute(query)
    patient = cursor.first()
    if patient is None:
        raise NotFoundException(message="пациент не найден!")

    return Patient.model_validate(patient[0])
