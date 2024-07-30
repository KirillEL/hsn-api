from shared.db import Transaction
from shared.db.db_session import session
from shared.db.models.patient import PatientDBModel
from shared.db.models.contragent import ContragentDBModel
from sqlalchemy import update, select

from loguru import logger

from shared.db.transaction import Propagation


async def delete_patient(payload: dict, patient_id: int):
    logger.info(f"Deleting patient")
    query = (
        update(PatientDBModel).where(PatientDBModel.id == patient_id).values(**payload)
    )

    await session.execute(query)


async def get_contragent_id(patient_id: int) -> int:
    logger.info(f"Getting contragent id")
    query_select = select(PatientDBModel.contragent_id).where(
        PatientDBModel.id == patient_id
    )
    cursor = await session.execute(query_select)
    contragent_id = cursor.scalar()
    return contragent_id


async def delete_contragent(payload: dict, contragent_id: int):
    logger.info(f"Deleting contragent")
    query_delete_contragent = (
        update(ContragentDBModel)
        .where(ContragentDBModel.id == contragent_id)
        .values(**payload)
    )
    await session.execute(query_delete_contragent)


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_patient_delete(patient_id: int, deleter_id: int):
    payload = {"deleter_id": deleter_id, "is_deleted": True}

    await delete_patient(payload=payload, patient_id=patient_id)

    contragent_id = await get_contragent_id(patient_id=patient_id)

    await delete_contragent(payload=payload, contragent_id=contragent_id)

    return None
