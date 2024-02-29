from .router import admin_medicine_prescription_router
from sqlalchemy import select
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from core.hsn.medicine_prescription import MedicinePrescription
from api.exceptions import ExceptionResponseSchema, NotFoundException


@admin_medicine_prescription_router.get(
    "/medicine_prescriptions/{medicine_prescription_id}",
    response_model=MedicinePrescription,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_prescription_by_id(medicine_prescription_id: int):
    query = (
        select(MedicinesPrescriptionDBModel)
        .where(MedicinesPrescriptionDBModel.id == medicine_prescription_id,
               MedicinesPrescriptionDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    med_prescription = cursor.scalars().first()
    if med_prescription is None:
        raise NotFoundException(message="не найдено!")
    return MedicinePrescription.model_validate(med_prescription)
