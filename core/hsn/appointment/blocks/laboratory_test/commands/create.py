from datetime import date as tdate

from sqlalchemy import insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from pydantic import BaseModel
from typing import Optional

from shared.db.models.appointment_laboratory_test import AppointmentLaboratoryTestDBModel


class HsnAppointmentBlockLaboratoryTestCreateContext(BaseModel):
    nt_pro_bnp: Optional[float] = None
    nt_pro_bnp_date: Optional[tdate] = None
    hbalc: Optional[float] = None
    hbalc_date: Optional[tdate] = None

    eritrocit: Optional[float] = None
    eritrocit_date: Optional[tdate] = None
    hemoglobin: Optional[float] = None
    hemoglobin_date: Optional[tdate] = None

    tg: Optional[float] = None
    tg_date: Optional[tdate] = None
    lpvp: Optional[float] = None
    lpvp_date: Optional[tdate] = None
    lpnp: Optional[float] = None
    lpnp_date: Optional[tdate] = None
    general_hc: Optional[float] = None
    general_hc_date: Optional[tdate] = None
    natriy: Optional[float] = None
    natriy_date: Optional[tdate] = None
    kaliy: Optional[float] = None
    kaliy_date: Optional[tdate] = None
    glukoza: Optional[float] = None
    glukoza_date: Optional[tdate] = None
    mochevaya_kislota: Optional[float] = None
    mochevaya_kislota_date: Optional[tdate] = None
    skf: Optional[float] = None
    skf_date: Optional[tdate] = None
    kreatinin: Optional[float] = None
    kreatinin_date: Optional[tdate] = None

    protein: Optional[float] = None
    protein_date: Optional[tdate] = None
    urine_eritrocit: Optional[float] = None
    urine_eritrocit_date: Optional[tdate] = None
    urine_leycocit: Optional[float] = None
    urine_leycocit_date: Optional[tdate] = None
    microalbumuria: Optional[float] = None
    microalbumuria_date: Optional[tdate] = None
    note: Optional[str] = None

@SessionContext()
async def hsn_appointment_block_laboratory_test_create(context: HsnAppointmentBlockLaboratoryTestCreateContext):
    query = (
        insert(AppointmentLaboratoryTestDBModel)
        .values(**context.model_dump())
        .returning(AppointmentLaboratoryTestBlockDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_block_laboratory_test_id = cursor.scalar()
    return new_block_laboratory_test_id