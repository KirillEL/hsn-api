from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import insert, exc

from api.exceptions import InternalServerException
from api.exceptions.base import UnprocessableEntityException
from core.hsn.medicine_prescription import MedicinePrescriptionFlat
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from shared.db.db_session import db_session, SessionContext


class HsnMedicinePrescriptionCreateContext(BaseModel):
    user_id: int = Field(gt=0)
    medicine_group: str
    name: str
    note: Optional[str] = None


@SessionContext()
async def hsn_medicine_prescription_create(context: HsnMedicinePrescriptionCreateContext):
    payload = context.model_dump(exclude={'user_id'}, exclude_none=True)

    query = (
        insert(MedicinesPrescriptionDBModel)
        .values(
            author_id=context.user_id,
            **payload
        )
        .returning(MedicinesPrescriptionDBModel)
    )
    cursor = await db_session.execute(query)
    try:
        await db_session.commit()
        new_med_prescription = cursor.scalars().first()

        return MedicinePrescriptionFlat.model_validate(new_med_prescription)
    except exc.SQLAlchemyError as sqle:
        await db_session.rollback()
        raise UnprocessableEntityException(message=str(sqle))
    except Exception as e:
        await db_session.rollback()
        raise InternalServerException
