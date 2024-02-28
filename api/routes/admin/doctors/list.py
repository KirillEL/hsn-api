from sqlalchemy import select
from .router import admin_doctor_router
from shared.db.models.doctor import DoctorDBModel
from core.hsn.doctor import Doctor
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext


@admin_doctor_router.get(
    "/doctors",
    response_model=list[Doctor],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_doctors_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(DoctorDBModel)
        .where(DoctorDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(DoctorDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    doctors = cursor.scalars().all()

    return [Doctor.model_validate(doc) for doc in doctors]
