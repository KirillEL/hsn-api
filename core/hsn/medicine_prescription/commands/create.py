from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import insert, exc, select
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import InternalServerException, NotFoundException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.medicine_prescription import MedicinePrescriptionFlat
from shared.db import Transaction
from shared.db.models.medicines_group import MedicinesGroupDBModel
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from shared.db.db_session import session
from shared.db.transaction import Propagation


class HsnMedicinePrescriptionCreateContext(BaseModel):
    user_id: int = Field(gt=0)
    medicine_group_id: int
    name: str
    note: Optional[str] = None


async def check_medicine_group_exists(medicine_group_id: int):
    query = (
        select(MedicinesGroupDBModel)
        .where(MedicinesGroupDBModel.id == medicine_group_id)
        .where(MedicinesGroupDBModel.is_deleted.is_(False))
    )
    cursor = await session.execute(query)
    med_group = cursor.scalar_one()
    if med_group is None:
        raise NotFoundException


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_medicine_prescription_create(
    context: HsnMedicinePrescriptionCreateContext,
):
    payload = context.model_dump(exclude={"user_id"}, exclude_none=True)
    await check_medicine_group_exists(context.medicine_group_id)
    query = (
        insert(MedicinesPrescriptionDBModel)
        .values(author_id=context.user_id, **payload)
        .returning(MedicinesPrescriptionDBModel.id)
    )
    cursor = await session.execute(query)
    medicine_prescription_id = cursor.scalar()

    query_select = (
        select(MedicinesPrescriptionDBModel)
        .options(selectinload(MedicinesPrescriptionDBModel.medicine_group))
        .where(MedicinesPrescriptionDBModel.id == medicine_prescription_id)
        .where(MedicinesPrescriptionDBModel.is_deleted.is_(False))
    )
    cursor = await session.execute(query_select)

    new_medicine_prescription = cursor.scalar_one()
    return MedicinePrescriptionFlat.model_validate(new_medicine_prescription)
