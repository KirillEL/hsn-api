from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from pydantic import BaseModel
from core.hsn.patient.model import Patient
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from api.exceptions import NotFoundException
from loguru import logger
from ..model import Contragent
from utils import contragent_hasher
from shared.db.models.contragent import ContragentDBModel


async def decode_contragent(contragent: ContragentDBModel):
    decoded_contragent = ContragentDBModel(
        phone_number=contragent_hasher.decrypt(contragent.phone_number),
        snils=contragent_hasher.decrypt(contragent.snils),
        address=contragent_hasher.decrypt(contragent.address),
        mis_number=contragent_hasher.decrypt(contragent.mis_number),
        date_birth=contragent_hasher.decrypt(contragent.date_birth),
        relative_phone_number=contragent_hasher.decrypt(contragent.relative_phone_number),
        parent=contragent_hasher.decrypt(contragent.parent),
        date_dead=contragent_hasher.decrypt(contragent.date_dead)
    )
    return decoded_contragent


@SessionContext()
async def hsn_patient_by_id(patient_id: int):
    pass
    query = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.contragent))
        .where(PatientDBModel.id == patient_id)
    )
    logger.debug(f"Query: {query}")
    if hasattr(PatientDBModel, "is_deleted"):
        query = query.where(PatientDBModel.is_deleted.is_(False))

    cursor = await db_session.execute(query)
    await db_session.commit()
    patient = cursor.scalars().first()
    if patient is None:
        raise NotFoundException(message="Пациент не найден!")
    patient.contragent = await decode_contragent(patient.contragent)
    return Patient.from_orm(patient)
