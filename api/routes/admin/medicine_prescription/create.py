from .router import admin_medicine_prescription_router
from sqlalchemy import select, insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from core.hsn.medicine_prescription import MedicinePrescription
from fastapi import Request


class CreateMedicinePrescriptionDto(BaseModel):
    pass


@admin_medicine_prescription_router.post(
    "/medicine_prescriptions",
    response_model=MedicinePrescription,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_medicine_prescription_create(request: Request, dto: CreateMedicinePrescriptionDto):
    query = (
        insert(MedicinesPrescriptionDBModel)
        .values(
            **dto.dict(),
            author_id=request.user.id
        )
        .returning(MedicinesPrescriptionDBModel)
    )
    cursor = await db_session.execute(query)
    new_med_prescription = cursor.scalars().first()

    return MedicinePrescription.model_validate(new_med_prescription)
