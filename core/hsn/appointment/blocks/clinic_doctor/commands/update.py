from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update, Select
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException, AppointmentNotBelongsToUserException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from shared.db.db_session import db_session, SessionContext


class HsnBlockClinicDoctorUpdateContext(BaseModel):
    appointment_id: int
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: Optional[str] = None
    lgota_drugs: Optional[str] = None
    has_hospitalization: Optional[bool] = None
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[str] = None


@SessionContext()
async def hsn_block_clinic_doctor_update(
        context: HsnBlockClinicDoctorUpdateContext,
        doctor_id: int = None
) -> AppointmentClinicDoctorBlock:
    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query: Select = (
        select(AppointmentDBModel.block_clinic_doctor_id, AppointmentDBModel.author_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    result = cursor.first()
    block_clinic_doctor_id, author_id = result
    if not block_clinic_doctor_id:
        raise NotFoundException(message="У приема нет этого блока!")

    if author_id != doctor_id:
        raise ForbiddenException(
            message="У вас нет прав на управление этим блоком"
        )

    query_update: ReturningUpdate = (
        update(AppointmentBlockClinicDoctorDBModel)
        .values(**payload)
        .where(AppointmentBlockClinicDoctorDBModel.id == block_clinic_doctor_id)
        .returning(AppointmentBlockClinicDoctorDBModel)
    )
    cursor: AsyncResult = await db_session.execute(query_update)
    await db_session.commit()
    update_block_clinic_doctor: AppointmentBlockClinicDoctorDBModel = cursor.scalars().first()
    return AppointmentClinicDoctorBlock.model_validate(update_block_clinic_doctor)
