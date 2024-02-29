from sqlalchemy import select
from .router import admin_doctor_router
from shared.db.models.doctor import DoctorDBModel
from core.hsn.doctor import Doctor
from api.exceptions import ExceptionResponseSchema, NotFoundException
from shared.db.db_session import db_session, SessionContext


@admin_doctor_router.get(
    "/doctors/{doctor_id}",
    response_model=Doctor,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_doctor_by_id(doctor_id: int):
    query = (
        select(DoctorDBModel)
        .where(DoctorDBModel.id == doctor_id, DoctorDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    doctor = cursor.scalars().first()
    if doctor is None:
        raise NotFoundException(message="Доктор не найден!")
    return Doctor.model_validate(doctor)
