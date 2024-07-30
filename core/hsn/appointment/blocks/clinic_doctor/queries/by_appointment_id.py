from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from shared.db.db_session import session
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinic_doctor import (
    AppointmentBlockClinicDoctorDBModel,
)
from sqlalchemy import select


async def hsn_get_block_clinic_doctor_by_appointment_id(appointment_id: int):
    query = (
        select(AppointmentDBModel.block_clinic_doctor_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await session.execute(query)
    block_clinic_doctor_id = cursor.scalar()
    if block_clinic_doctor_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = select(AppointmentBlockClinicDoctorDBModel).where(
        AppointmentBlockClinicDoctorDBModel.id == block_clinic_doctor_id
    )
    cursor = await session.execute(query_get_block)
    block_clinic_doctor = cursor.scalars().first()
    return AppointmentClinicDoctorBlock.model_validate(block_clinic_doctor)
