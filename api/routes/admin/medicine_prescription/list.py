from .router import admin_medicine_prescription_router
from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from api.exceptions import ExceptionResponseSchema
from core.hsn.medicine_prescription import MedicinePrescription


@admin_medicine_prescription_router.get(
    "/medicine_prescriptions",
    response_model=list[MedicinePrescription],
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_prescriptions_list(limit: int = None, offset: int = None, pattern: str = None):
    query = (
        select(MedicinesPrescriptionDBModel)
        .where(MedicinesPrescriptionDBModel.is_deleted.is_(False))
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if pattern is not None:
        query = query.where(MedicinesPrescriptionDBModel.name.contains(pattern))

    cursor = await db_session.execute(query)
    med_prescriptions = cursor.scalars().all()

    return [MedicinePrescription.model_validate(med_p) for med_p in med_prescriptions]
