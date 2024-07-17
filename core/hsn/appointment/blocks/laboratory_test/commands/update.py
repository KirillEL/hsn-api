from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select, update

from api.decorators import HandleExceptions
from api.exceptions import NotFoundException
from core.hsn.appointment.blocks.laboratory_test import AppointmentLaboratoryTestBlock
from shared.db import Transaction
from shared.db.models.appointment.appointment import AppointmentDBModel
from shared.db.models.appointment.blocks.block_laboratory_test import AppointmentLaboratoryTestBlockDBModel
from shared.db.db_session import session
from shared.db.transaction import Propagation


class HsnBlockLaboratoryTestUpdateContext(BaseModel):
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


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_block_laboratory_test_update(context: HsnBlockLaboratoryTestUpdateContext):
    payload = context.model_dump(exclude={'appointment_id'}, exclude_none=True)

    query = (
        select(AppointmentDBModel.block_laboratory_test_id)
        .where(AppointmentDBModel.is_deleted.is_(False))
        .where(AppointmentDBModel.id == context.appointment_id)
    )
    cursor = await session.execute(query)
    block_laboratory_test_id = cursor.scalar()
    if block_laboratory_test_id is None:
        raise NotFoundException(message="У приема нет данного блока!")

    query_update = (
        update(AppointmentLaboratoryTestBlockDBModel)
        .values(**payload)
        .where(AppointmentLaboratoryTestBlockDBModel.id == block_laboratory_test_id)
        .returning(AppointmentLaboratoryTestBlockDBModel)
    )
    cursor = await session.execute(query_update)
    updated_block_laboratory_test = cursor.scalars().first()
    return AppointmentLaboratoryTestBlock.model_validate(updated_block_laboratory_test)
