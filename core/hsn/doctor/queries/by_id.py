from sqlalchemy import select
from shared.db.models.doctor import DoctorDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_query_doctor_by_id(doctor_id: int):
    query = select([DoctorDBModel])

    if hasattr(DoctorDBModel, 'is_deleted'):
        query = query.where(DoctorDBModel.is_deleted.is_(False))

    query = query.where(DoctorDBModel.id == doctor_id)
    cursor = await db_session.execute(query)
    result = cursor.first()

    return None if result is None else result[DoctorDBModel]
