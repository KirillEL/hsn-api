from typing import Optional

from sqlalchemy import insert, update, exc, Result, Update
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.sql.dml import ReturningInsert

from api.exceptions import NotFoundException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_complaint import AppointmentComplaintBlockDBModel
from pydantic import BaseModel

from shared.db.queries import db_query_entity_by_id


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
async def hsn_command_appointment_block_complaint_create(
        context: HsnCommandAppointmentBlockComplaintCreateContext
) -> int:
    appointment: AppointmentDBModel = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)
    if not appointment:
        raise NotFoundException("Прием не найден")

    payload = context.model_dump(exclude={'appointment_id'})
    query: ReturningInsert = (
        insert(AppointmentComplaintBlockDBModel)
        .values(**payload)
        .returning(AppointmentComplaintBlockDBModel.id)
    )
    cursor: AsyncResult = await db_session.execute(query)
    new_complaint_block_id: int = cursor.scalar()

    query_update_appointment: Update = (
        update(AppointmentDBModel)
        .values(
            block_complaint_id=new_complaint_block_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()

    return new_complaint_block_id
