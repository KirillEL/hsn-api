from sqlalchemy import insert, update, exc
from pydantic import BaseModel
from typing import Optional

from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import check_appointment_exists
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_ekg import AppointmentEkgBlockDBModel
from datetime import date as tdate

class HsnAppointmentBlockEkgCreateContext(BaseModel):
    appointment_id: int
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
    try:
        await check_appointment_exists(context.appointment_id)
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
    except NotFoundException as ne:
        await db_session.rollback()
        raise ne
    except exc.SQLAlchemyError as sqle:
        await db_session.rollback()
        raise UnprocessableEntityException(message=str(sqle))
    except Exception as e:
        await db_session.rollback()
        raise InternalServerException(message=str(e))