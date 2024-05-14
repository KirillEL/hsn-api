from typing import Optional

from sqlalchemy import insert, update, select, exc

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from pydantic import BaseModel
from datetime import date as tdate


class HsnAppointmentBlockClinicDoctorCreateContext(BaseModel):
    appointment_id: int
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: Optional[bool] = False
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[tdate] = None


async def check_appointment_exists(appointment_id: int):
    query = (
        select(AppointmentDBModel)
        .where(AppointmentDBModel.id == appointment_id)
    )
    cursor = await db_session.execute(query)
    appointment = cursor.scalars().first()
    if appointment is None:
        raise NotFoundException(message="Прием не найден!")


@SessionContext()
@HandleExceptions()
async def hsn_appointment_block_clinic_doctor_create(context: HsnAppointmentBlockClinicDoctorCreateContext):
    await check_appointment_exists(context.appointment_id)
    payload = context.model_dump(exclude={'appointment_id'})
    query = (
        insert(AppointmentBlockClinicDoctorDBModel)
        .values(**payload)
        .returning(AppointmentBlockClinicDoctorDBModel.id)
    )
    cursor = await db_session.execute(query)
    new_block_clinic_doctor_id = cursor.scalar()

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(
            block_clinic_doctor_id=new_block_clinic_doctor_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()
    return new_block_clinic_doctor_id
