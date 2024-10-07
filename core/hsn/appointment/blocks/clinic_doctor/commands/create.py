from typing import Optional

from sqlalchemy import insert, update, select, exc

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
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
    last_hospitalization_date: Optional[tdate] = None


@SessionContext()
async def hsn_command_appointment_block_clinic_doctor_create(
        context: HsnCommandAppointmentBlockClinicDoctorCreateContext
):
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)

    if not appointment:
        raise NotFoundException(
            message="Прием не найден"
        )

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
