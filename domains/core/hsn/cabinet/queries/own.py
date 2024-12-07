from domains.shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from domains.shared.db.models.doctor import DoctorDBModel
from domains.core.hsn.cabinet import Cabinet
from loguru import logger


@SessionContext()
async def hsn_cabinet_own(doctor_id: int):
    logger.info(f"Cabinet own")
    query = (
        select(DoctorDBModel)
        .options(joinedload(DoctorDBModel.cabinet))
        .where(DoctorDBModel.id == doctor_id)
    )
    logger.info(f"query: {query}")
    cursor = await db_session.execute(query)
    doctor = cursor.scalars().first()
    logger.info(f"doctor: {doctor.__dict__}")
    cabinet = doctor.cabinet
    logger.info(f"cabinet: {cabinet.__dict__}")
    return Cabinet.model_validate(cabinet)
