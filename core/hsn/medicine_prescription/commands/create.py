from typing import Optional

from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import insert, exc, select
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import InternalServerException, NotFoundException, MedicinePrescriptionCreateException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.medicine_prescription import MedicinePrescriptionFlat
from core.hsn.medicine_prescription.model import MedicinePrescriptionFlatResponse
from shared.db.models.medicines_group import MedicinesGroupDBModel
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from shared.db.db_session import db_session, SessionContext


class HsnMedicinePrescriptionCreateContext(BaseModel):
    doctor_id: int = Field(gt=0)  # id текущего врача
    medicine_group_id: int
    name: str
    note: Optional[str] = None


async def check_medicine_group_exists(medicine_group_id: int):
    query = (
        select(MedicinesGroupDBModel)
        .where(MedicinesGroupDBModel.id == medicine_group_id)
        .where(MedicinesGroupDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    med_group = cursor.scalar_one()
    if med_group is None:
        raise NotFoundException


@SessionContext()
@HandleExceptions()
async def hsn_medicine_prescription_create(
        context: HsnMedicinePrescriptionCreateContext) -> MedicinePrescriptionFlatResponse:
    payload = context.model_dump(exclude={'doctor_id'}, exclude_none=True)
    await check_medicine_group_exists(context.medicine_group_id)
    query = (
        insert(MedicinesPrescriptionDBModel)
        .values(
            author_id=context.doctor_id,
            **payload
        )
        .returning(MedicinesPrescriptionDBModel.id)
    )
    try:
        cursor = await db_session.execute(query)
        await db_session.commit()
    except exc.SQLAlchemyError as sqle:
        logger.error(f"Failed to create med_prescription: {sqle}")
        raise MedicinePrescriptionCreateException

    medicine_prescription_id = cursor.scalar()

    query_select = (
        select(MedicinesPrescriptionDBModel)
        .options(selectinload(MedicinesPrescriptionDBModel.medicine_group))
        .where(MedicinesPrescriptionDBModel.id == medicine_prescription_id)
    )

    if hasattr(MedicinesPrescriptionDBModel, "is_deleted"):
        query_select = query_select.where(
            MedicinesPrescriptionDBModel.is_deleted.is_(False)
        )
    try:
        cursor = await db_session.execute(query_select)
    except exc.SQLAlchemyError as sqle:
        logger.error(f"Failed to get created med_prescription: {sqle}")
        raise NotFoundException

    new_medicine_prescription = cursor.scalar_one()
    return MedicinePrescriptionFlatResponse.model_validate(new_medicine_prescription)
