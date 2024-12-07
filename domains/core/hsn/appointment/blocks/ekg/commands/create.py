from sqlalchemy import insert, update, Result, Update
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.sql.dml import ReturningInsert

from api.exceptions import NotFoundException
from api.exceptions.base import ForbiddenException
from domains.shared.db.db_session import db_session, SessionContext
from domains.shared.db.models.appointment.appointment import AppointmentDBModel
from domains.shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel

from domains.shared.db.queries import db_query_entity_by_id


class HsnCommandAppointmentBlockEkgCreateContext(BaseModel):
    appointment_id: int
    date_ekg: Optional[str] = None
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
    fv: float
    sdla: Optional[float] = None
    lp: Optional[float] = None
    lp2: Optional[float] = None
    pp: Optional[float] = None
    pp2: Optional[float] = None
    kdr_lg: Optional[float] = None
    ksr_lg: Optional[float] = None
    kdo_lg: Optional[float] = None
    kso_lg: Optional[float] = None
    mgp: Optional[float] = None
    zslg: Optional[float] = None

    local_hypokines: Optional[bool] = False
    difusal_hypokines: Optional[bool] = False
    distol_disfunction: Optional[bool] = False
    valvular_lesions: Optional[bool] = False
    anevrizma: Optional[bool] = False
    note: Optional[str] = None


@SessionContext()
async def hsn_command_appointment_block_ekg_create(
    doctor_id: int, context: HsnCommandAppointmentBlockEkgCreateContext
) -> int:
    appointment = await db_query_entity_by_id(
        AppointmentDBModel, context.appointment_id
    )
    if not appointment:
        raise NotFoundException(
            message="Прием c id:{} не найден".format(context.appointment_id)
        )

    if appointment.doctor_id != doctor_id:
        raise ForbiddenException(
            "У вас нет прав для доступа к приему с id:{}".format(context.appointment_id)
        )

    payload = context.model_dump(exclude={"appointment_id"})

    query: ReturningInsert = (
        insert(AppointmentEkgBlockDBModel)
        .values(**payload)
        .returning(AppointmentEkgBlockDBModel.id)
    )
    cursor: Result = await db_session.execute(query)
    new_block_ekg_id: int = cursor.scalar()

    query_update_appointment: Update = (
        update(AppointmentDBModel)
        .values(block_ekg_id=new_block_ekg_id)
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)

    await db_session.commit()
    return new_block_ekg_id
