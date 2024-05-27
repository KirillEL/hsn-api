from typing import Optional

from api.decorators import HandleExceptions
from core.hsn.cabinet.model import CabinetFlat
from core.hsn.patient.commands.create import convert_to_patient_response
from core.hsn.patient.model import PatientFlat, BasePatientResponse, Contragent, PatientResponseWithoutFullName
from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import select
from sqlalchemy.orm import joinedload


@admin_patient_router.get(
    "/patients",
    response_model=list[PatientResponseWithoutFullName],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
@HandleExceptions()
async def admin_patients_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.contragent), joinedload(PatientDBModel.cabinet))
        .where(PatientDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(PatientDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    patients = cursor.scalars().all()
    converted_patients = []
    for patient in patients:
        patient = await convert_to_patient_response(patient, type="without")
        converted_patients.append(patient)
    return converted_patients
