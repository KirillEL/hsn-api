from sqlalchemy.ext.asyncio import AsyncResult

from api.exceptions import NotFoundException, AppointmentNotBelongsToUserException
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from sqlalchemy import select, Select


@SessionContext()
async def hsn_get_block_clinic_doctor_by_appointment_id(
        appointment_id: int,
        user_id: int = None
) -> AppointmentClinicDoctorBlock:
    query: Select = (
        select(AppointmentDBModel.block_clinic_doctor_id, AppointmentDBModel.author_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    result = cursor.first()
    block_clinic_doctor_id, author_id = result
    if not block_clinic_doctor_id:
        raise NotFoundException(message="У приема нет данного блока!")

    if author_id != user_id:
        raise AppointmentNotBelongsToUserException

    query_get_block: Select = (
        select(AppointmentBlockClinicDoctorDBModel)
        .where(AppointmentBlockClinicDoctorDBModel.id == block_clinic_doctor_id)
    )
    cursor: AsyncResult = await db_session.execute(query_get_block)
    block_clinic_doctor: AppointmentBlockClinicDoctorDBModel = cursor.scalars().first()
    return AppointmentClinicDoctorBlock.model_validate(block_clinic_doctor)
