from sqlalchemy import insert
from pydantic import BaseModel
from typing import Optional
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from datetime import date as tdate

class HsnAppointmentBlockEkgCreateContext(BaseModel):
    date_ekg: tdate
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
    date_echo_ekg: tdate
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
async def hsn_appointment_block_ekg_create(context: HsnAppointmentBlockEkgCreateContext):
    query = (
        insert(AppointmentEkgBlockDBModel)
        .values(**context.model_dump())
        .returning(AppointmentEkgBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_block_ekg_id = cursor.scalar()
    return new_block_ekg_id
