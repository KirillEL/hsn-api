from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel
from ..schemas import ClinicalAssesment
from typing import Optional
from shared.db.models.clinical_assesment import ClinicalAssesmentDBModel
from sqlalchemy import select
from api.exceptions import NotFoundException


@SessionContext()
async def hsn_clinical_assesment_get_by_patient_appointment_id(patient_appointment_id: int) -> Optional[
    ClinicalAssesment]:
    query = (
        select(ClinicalAssesmentDBModel)
        .where(ClinicalAssesmentDBModel.patient_appointment_id == patient_appointment_id)
    )
    cursor = await db_session.execute(query)
    res = cursor.first()
    if res is None:
        raise NotFoundException(message="такой не найден!")

    return ClinicalAssesment.model_validate(res[0])
