from sqlalchemy import insert, update, exc
from pydantic import BaseModel
from typing import Optional

from api.exceptions import NotFoundException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from datetime import date as tdate

from shared.db.queries import db_query_entity_by_id


class HsnCommandAppointmentBlockEkgCreateContext(BaseModel):
    appointment_id: int
    date_ekg: str
    sinus_ritm: Optional[bool] = False
    av_blokada: Optional[bool] = False
    hypertrofia_lg: Optional[bool] = False
    ritm_eks: Optional[bool] = False
    av_uzlovaya_tahikardia: Optional[bool] = False
    superventrikulyrnaya_tahikardia: Optional[bool] = False
    zheludochnaya_tahikardia: Optional[bool] = False
    fabrilycia_predcerdiy: Optional[bool] = False
    trepetanie_predcerdiy: Optional[bool] = False
    another_changes: Optional[str] = None
    date_echo_ekg: str
    fv: int
    sdla: Optional[int] = None
    lp: Optional[int] = None
    pp: Optional[int] = None
    kdr_lg: Optional[int] = None
    ksr_lg: Optional[int] = None
    kdo_lg: Optional[int] = None
    mgp: Optional[int] = None
    zslg: Optional[int] = None

    local_hypokines: Optional[bool] = False
    distol_disfunction: Optional[bool] = False
    anevrizma: Optional[bool] = False
    note: Optional[str] = None


@SessionContext()
async def hsn_command_appointment_block_ekg_create(
        context: HsnCommandAppointmentBlockEkgCreateContext
):
    appointment = await db_query_entity_by_id(AppointmentDBModel, context.appointment_id)
    if not appointment:
        raise NotFoundException(message="Прием не найден")

    payload = context.model_dump(exclude={'appointment_id'})
    query = (
        insert(AppointmentEkgBlockDBModel)
        .values(**payload)
        .returning(AppointmentEkgBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    new_block_ekg_id = cursor.scalar()

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(
            block_ekg_id=new_block_ekg_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()
    return new_block_ekg_id
