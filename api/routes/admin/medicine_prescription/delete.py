from .router import admin_medicine_prescription_router
from sqlalchemy import select, update
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
# add medicine prescription to core.hsn
from api.exceptions import ExceptionResponseSchema
from fastapi import Request


@admin_medicine_prescription_router.delete(
    "/medicine_prescriptions/{medicine_prescription_id}",
    response_model=bool,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_prescription_delete(medicine_prescription_id: int, request: Request):
    payload = {
        'is_deleted': True,
        'deleter_id': request.user.id
    }
    query = (
        update(MedicinesPrescriptionDBModel)
        .values(
            **payload
        )
        .where(MedicinesPrescriptionDBModel.id == medicine_prescription_id)
    )
    await db_session.execute(query)
    await db_session.commit()
    return True