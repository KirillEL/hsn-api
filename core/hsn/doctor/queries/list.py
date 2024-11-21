from sqlalchemy import select

from api.decorators import HandleExceptions
from shared.db.models.doctor import DoctorDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
@HandleExceptions()
async def hsn_query_doctor_list(
    limit: int = None, offset: int = None, pattern: str = None
):
    query = select(DoctorDBModel)

    if hasattr(DoctorDBModel, "is_deleted"):
        query = query.where(DoctorDBModel.is_deleted.is_(False))

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(DoctorDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    return [item for item in cursor.scalars().all()]
