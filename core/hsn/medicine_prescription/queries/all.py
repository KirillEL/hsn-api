from sqlalchemy import select
from sqlalchemy.orm import selectinload

from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from core.hsn.medicine_prescription import MedicinePrescriptionFlat


@SessionContext()
async def hsn_medicine_prescription_all(limit: int = None, offset: int = None):
    query = (
        select(MedicinesPrescriptionDBModel)
        .options(selectinload(MedicinesPrescriptionDBModel.medicine_group))
        .where(MedicinesPrescriptionDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    medicine_prescriptions = cursor.scalars().all()

    return [MedicinePrescriptionFlat.model_validate(m_p) for m_p in medicine_prescriptions]
