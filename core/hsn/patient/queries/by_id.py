from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel
from core.hsn.patient.model import Patient
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from api.exceptions import NotFoundException
from loguru import logger
from utils import cipher


@SessionContext()
async def hsn_patient_by_id(patient_id: int):
    query = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.contragent))
        .where(PatientDBModel.id == patient_id)
    )
    logger.debug(f'query: {query}')
    if hasattr(PatientDBModel, "is_deleted"):
        query = query.where(PatientDBModel.is_deleted.is_(False))

    cursor = await db_session.execute(query)
    patient = cursor.scalars().first()
    patient.contragent.phone_number = int(cipher.decrypt(patient.contragent.phone_number))
    patient.contragent.snils = str(cipher.decrypt(patient.contragent.snils))
    patient.contragent.address = str(cipher.decrypt(patient.contragent.address))
    patient.contragent.mis_number = int(cipher.decrypt(patient.contragent.mis_number))
    patient.contragent.date_birth = str(cipher.decrypt(patient.contragent.date_birth))
    patient.contragent.relative_phone_number = int(cipher.decrypt(patient.contragent.relative_phone_number))
    patient.contragent.parent = str(cipher.decrypt(patient.contragent.parent))
    patient.contragent.date_dead = str(cipher.decrypt(patient.contragent.date_dead))
    logger.debug(f'data: {patient}')
    if patient is None:
        raise NotFoundException(message="пациент не найден!")

    return Patient.model_validate(patient)
