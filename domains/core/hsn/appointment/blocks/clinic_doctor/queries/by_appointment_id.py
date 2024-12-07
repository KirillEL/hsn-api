from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from domains.core.hsn.appointment.blocks.clinic_doctor import AppointmentClinicDoctorBlock
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from domains.shared.db.models.appointment.blocks.block_clinic_doctor import (
    AppointmentBlockClinicDoctorDBModel,
)
from sqlalchemy import select, Select, Result

from domains.shared.db.queries import db_query_entity_by_id


@SessionContext()
async def hsn_get_block_clinic_doctor_by_appointment_id(
    doctor_id: int,
    appointment_id: int,
) -> AppointmentClinicDoctorBlock | None:
    appointment = await db_query_entity_by_id(AppointmentDBModel, appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            "У приема нет прав для доступа к приему с id:{}".format(appointment_id)
        )

    query: Select = (
        select(AppointmentDBModel.block_clinic_doctor_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor: Result = await db_session.execute(query)
    block_clinic_doctor_id = cursor.scalar()

    if not block_clinic_doctor_id:
        return None

    query_get_block: Select = select(AppointmentBlockClinicDoctorDBModel).where(
        AppointmentBlockClinicDoctorDBModel.id == block_clinic_doctor_id
    )
    cursor: Result = await db_session.execute(query_get_block)
    block_clinic_doctor: AppointmentBlockClinicDoctorDBModel = cursor.scalars().first()

    return AppointmentClinicDoctorBlock.model_validate(block_clinic_doctor)
