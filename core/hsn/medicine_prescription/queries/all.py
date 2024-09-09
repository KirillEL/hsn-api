from loguru import logger
from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload

from api.decorators import HandleExceptions
from api.exceptions import InternalServerException
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from core.hsn.medicine_prescription import MedicinePrescriptionFlat


@SessionContext()
@HandleExceptions()
async def hsn_medicine_prescription_all(limit: int = None, offset: int = None):
    query = (
        select(MedicinesPrescriptionDBModel)
        .options(selectinload(MedicinesPrescriptionDBModel.medicine_group))
        .where(MedicinesPrescriptionDBModel.is_deleted.is_(False))
    )
    try:
        cursor = await db_session.execute(query)
        medicine_prescriptions = cursor.scalars().all()
    except exc.SQLAlchemyError as sqle:
        logger.error(f"Failed to get med_prescriptions: {sqle}")
        raise InternalServerException

    return [MedicinePrescriptionFlat.model_validate(m_p) for m_p in medicine_prescriptions]
