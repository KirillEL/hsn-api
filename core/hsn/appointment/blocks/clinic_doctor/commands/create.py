from typing import Optional

from sqlalchemy import insert, update, select, exc, Update, Result
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningInsert

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException, ForbiddenException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from pydantic import BaseModel
from datetime import date as tdate

from shared.db.queries import db_query_entity_by_id


class HsnCommandAppointmentBlockClinicDoctorCreateContext(BaseModel):
    appointment_id: int
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: Optional[bool] = False
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[str] = None


@SessionContext()
async def hsn_command_appointment_block_clinic_doctor_create(
        doctor_id: int,
        context: HsnCommandAppointmentBlockClinicDoctorCreateContext
) -> int:
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException("Прием с id:{} не найден".format(context.appointment_id))

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException("У вас нет прав для доступа к приему с id:{}".format(context.appointment_id))

    payload = context.model_dump(exclude={'appointment_id'})

    query: ReturningInsert = (
        insert(AppointmentBlockClinicDoctorDBModel)
        .values(**payload)
        .returning(AppointmentBlockClinicDoctorDBModel.id)
    )
    cursor: Result = await db_session.execute(query)
    new_block_clinic_doctor_id: int = cursor.scalar()

    query_update_appointment: Update = (
        update(AppointmentDBModel)
        .values(
            block_clinic_doctor_id=new_block_clinic_doctor_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()
    return new_block_clinic_doctor_id
