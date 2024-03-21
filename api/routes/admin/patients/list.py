from core.hsn.patient.model import PatientFlat
from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from utils.hash_helper import contragent_hasher


@admin_patient_router.get(
    "/patients",
    response_model=list[PatientFlat],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
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
    for patient in patients:
        patient.contragent.phone_number = contragent_hasher.decrypt(patient.contragent.phone_number)
        patient.contragent.snils = contragent_hasher.decrypt(patient.contragent.snils)
        patient.contragent.address = contragent_hasher.decrypt(patient.contragent.address)
        patient.contragent.mis_number = contragent_hasher.decrypt(patient.contragent.mis_number)
        patient.contragent.date_birth = contragent_hasher.decrypt(patient.contragent.date_birth)
        patient.contragent.relative_phone_number = contragent_hasher.decrypt(patient.contragent.relative_phone_number)
        patient.contragent.parent = contragent_hasher.decrypt(patient.contragent.parent)
        patient.contragent.date_dead = contragent_hasher.decrypt(patient.contragent.date_dead)

    return [PatientFlat.model_validate(patient) for patient in patients]
