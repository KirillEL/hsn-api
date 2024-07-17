from shared.db.db_session import session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from shared.db.models.doctor import DoctorDBModel
from core.hsn.cabinet import Cabinet
from loguru import logger


async def hsn_cabinet_own(doctor_id: int):
    query = (
        select(DoctorDBModel)
        .options(joinedload(DoctorDBModel.cabinet))
        .where(DoctorDBModel.id == doctor_id)
    )
    cursor = await session.execute(query)
    doctor = cursor.scalars().first()
    cabinet = doctor.cabinet
    return Cabinet.model_validate(cabinet)
