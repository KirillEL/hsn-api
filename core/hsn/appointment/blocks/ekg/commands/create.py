from sqlalchemy import insert, update, exc
from pydantic import BaseModel
from typing import Optional

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import (
    check_appointment_exists,
)
from shared.db import Transaction
from shared.db.db_session import session
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from datetime import date as tdate

from shared.db.transaction import Propagation


class HsnAppointmentBlockEkgCreateContext(BaseModel):
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


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_appointment_block_ekg_create(
    context: HsnAppointmentBlockEkgCreateContext,
):
    await check_appointment_exists(context.appointment_id)
    payload = context.model_dump(exclude={"appointment_id"})
    query = (
        insert(AppointmentEkgBlockDBModel)
        .values(**payload)
        .returning(AppointmentEkgBlockDBModel.id)
    )
    cursor = await session.execute(query)
    new_block_ekg_id = cursor.scalar()

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(block_ekg_id=new_block_ekg_id)
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await session.execute(query_update_appointment)

    return new_block_ekg_id
