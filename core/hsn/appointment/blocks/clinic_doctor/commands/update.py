from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update, Select, Result
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningUpdate

from api.exceptions import NotFoundException, AppointmentNotBelongsToUserException
from api.exceptions.base import ForbiddenException
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from shared.db.db_session import db_session, SessionContext
from shared.db.queries import db_query_entity_by_id


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
        doctor_id: int,
        context: HsnBlockClinicDoctorUpdateContext
) -> AppointmentClinicDoctorBlock:
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(context.appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(context.appointment_id))

    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query: Select = (
        select(AppointmentDBModel.block_clinic_doctor_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_clinic_doctor_id: int = cursor.scalar()

    if not block_clinic_doctor_id:
        raise NotFoundException(message="У приема с id:{} нет данного блока".format(context.appointment_id))

    query_update: ReturningUpdate = (
        update(AppointmentBlockClinicDoctorDBModel)
        .values(**payload)
        .where(AppointmentBlockClinicDoctorDBModel.id == block_clinic_doctor_id)
        .returning(AppointmentBlockClinicDoctorDBModel)
    )
    cursor: Result = await db_session.execute(query_update)
    await db_session.commit()
    update_block_clinic_doctor: AppointmentBlockClinicDoctorDBModel = cursor.scalars().first()

    return AppointmentClinicDoctorBlock.model_validate(update_block_clinic_doctor)
