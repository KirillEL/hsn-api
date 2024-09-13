from datetime import date as tdate, datetime

from loguru import logger
from sqlalchemy import insert, update, exc

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException, InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.appointment.blocks.clinic_doctor.commands.create import check_appointment_exists
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from pydantic import BaseModel
from typing import Optional

from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel


class HsnAppointmentBlockLaboratoryTestCreateContext(BaseModel):
    appointment_id: int

    nt_pro_bnp: Optional[float] = None
    nt_pro_bnp_date: Optional[str] = None
    hbalc: Optional[float] = None
    hbalc_date: Optional[str] = None

    eritrocit: Optional[float] = None
    eritrocit_date: Optional[str] = None
    hemoglobin: Optional[float] = None
    hemoglobin_date: Optional[str] = None

    tg: Optional[float] = None
    tg_date: Optional[str] = None
    lpvp: Optional[float] = None
    lpvp_date: Optional[str] = None
    lpnp: Optional[float] = None
    lpnp_date: Optional[str] = None
    general_hc: Optional[float] = None
    general_hc_date: Optional[str] = None
    natriy: Optional[float] = None
    natriy_date: Optional[str] = None
    kaliy: Optional[float] = None
    kaliy_date: Optional[str] = None
    glukoza: Optional[float] = None
    glukoza_date: Optional[str] = None
    mochevaya_kislota: Optional[float] = None
    mochevaya_kislota_date: Optional[str] = None
    skf: Optional[float] = None
    skf_date: Optional[str] = None
    kreatinin: Optional[float] = None
    kreatinin_date: Optional[str] = None

    protein: Optional[float] = None
    protein_date: Optional[str] = None
    urine_eritrocit: Optional[float] = None
    urine_eritrocit_date: Optional[str] = None
    urine_leycocit: Optional[float] = None
    urine_leycocit_date: Optional[str] = None
    microalbumuria: Optional[float] = None
    microalbumuria_date: Optional[str] = None
    note: Optional[str] = None


@SessionContext()
async def hsn_appointment_block_laboratory_test_create(context: HsnAppointmentBlockLaboratoryTestCreateContext):
    await check_appointment_exists(context.appointment_id)
    payload = context.model_dump(exclude={'appointment_id'})
    query = (
        insert(AppointmentLaboratoryTestBlockDBModel)
        .values(**payload)
        .returning(AppointmentLaboratoryTestBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    new_block_laboratory_test_id = cursor.scalar()

    query_update_appointment = (
        update(AppointmentDBModel)
        .values(
            block_laboratory_test_id=new_block_laboratory_test_id
        )
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    await db_session.execute(query_update_appointment)
    await db_session.commit()

    return new_block_laboratory_test_id
