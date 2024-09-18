from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update

from api.exceptions import NotFoundException, AppointmentNotBelongsToUserException
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
async def hsn_block_clinic_doctor_update(context: HsnBlockClinicDoctorUpdateContext, user_id: int = None):
    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query = (
        select(AppointmentDBModel.block_clinic_doctor_id, AppointmentDBModel.author_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor = await db_session.execute(query)
    result = cursor.first()
    block_clinic_doctor_id, author_id = result
    if block_clinic_doctor_id is None:
        raise NotFoundException(message="У приема нет этого блока!")

    if author_id != user_id:
        raise AppointmentNotBelongsToUserException

    query_update = (
        update(AppointmentBlockClinicDoctorDBModel)
        .values(**payload)
        .where(AppointmentBlockClinicDoctorDBModel.id == block_clinic_doctor_id)
        .returning(AppointmentBlockClinicDoctorDBModel)
    )
    cursor = await db_session.execute(query_update)
    await db_session.commit()
    update_block_clinic_doctor = cursor.scalars().first()
    return AppointmentClinicDoctorBlock.model_validate(update_block_clinic_doctor)
