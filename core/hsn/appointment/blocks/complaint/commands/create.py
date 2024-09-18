from typing import Optional

from sqlalchemy import insert, update, exc

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import check_appointment_exists
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from pydantic import BaseModel


class HsnCommandAppointmentBlockComplaintCreateContext(BaseModel):
    appointment_id: int
    has_fatigue: Optional[bool] = False
    has_dyspnea: Optional[bool] = False
    has_swelling_legs: Optional[bool] = False
    has_weakness: Optional[bool] = False
    has_orthopnea: Optional[bool] = False
    has_heartbeat: Optional[bool] = True
    note: Optional[str] = False


@SessionContext()
async def hsn_command_appointment_block_complaint_create(context: HsnCommandAppointmentBlockComplaintCreateContext) -> int:
    await check_appointment_exists(context.appointment_id)
    payload = context.model_dump(exclude={'appointment_id'})
    query = (
        insert(AppointmentComplaintBlockDBModel)
        .values(**payload)
        .returning(AppointmentComplaintBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    new_complaint_block_id = cursor.scalar()

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(
            block_complaint_id=new_complaint_block_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()

    return new_complaint_block_id
