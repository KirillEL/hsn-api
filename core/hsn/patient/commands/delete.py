from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient import PatientDBModel
from shared.db.models.contragent import ContragentDBModel
from sqlalchemy import update, select

from loguru import logger


async def delete_patient(payload: dict, patient_id: int):
    logger.info(f"Deleting patient")
    query = (
        update(PatientDBModel).where(PatientDBModel.id == patient_id).values(**payload)
    )

    await db_session.execute(query)


async def get_contragent_id(patient_id: int) -> int:
    logger.info(f"Getting contragent id")
    query_select = select(PatientDBModel.contragent_id).where(
        PatientDBModel.id == patient_id
    )
    cursor = await db_session.execute(query_select)
    contragent_id = cursor.scalar()
    return contragent_id


async def delete_contragent(payload: dict, contragent_id: int):
    logger.info(f"Deleting contragent")
    query_delete_contragent = (
        update(ContragentDBModel)
        .where(ContragentDBModel.id == contragent_id)
        .values(**payload)
    )
    await db_session.execute(query_delete_contragent)


@SessionContext()
async def hsn_patient_delete(patient_id: int, deleter_id: int):
    payload = {"deleter_id": deleter_id, "is_deleted": True}

    await delete_patient(payload=payload, patient_id=patient_id)

    contragent_id = await get_contragent_id(patient_id=patient_id)

    await delete_contragent(payload=payload, contragent_id=contragent_id)

    await db_session.commit()
    return None
