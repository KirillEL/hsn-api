from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from sqlalchemy import select

@SessionContext()
async def hsn_get_block_clinic_doctor_by_appointment_id(appointment_id:int):
    query = (
        select(AppointmentDBModel.block_clinic_doctor_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    block_clinic_doctor_id = cursor.scalar()
    if block_clinic_doctor_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_get_block = (
        select(AppointmentBlockClinicDoctorDBModel)
        .where(AppointmentBlockClinicDoctorDBModel.id == block_clinic_doctor_id)
    )
    cursor = await db_session.execute(query_get_block)
    block_clinic_doctor = cursor.scalars().first()
    return AppointmentClinicDoctorBlock.model_validate(block_clinic_doctor)