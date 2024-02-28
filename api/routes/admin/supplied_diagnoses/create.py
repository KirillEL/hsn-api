from typing import Optional

from .router import admin_supplied_diagnose_router
from sqlalchemy import select, insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.supplied_diagnoses import SuppliedDiagnosesDBModel
from core.hsn.supplied_diagnoses.model import SuppliedDiagnoses
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field
from fastapi import Request


class CreateSuppliedDiagnoseDto(BaseModel):
    patient_appointment_id: int = Field(gt=0)
    diagnose_catalog_id: int = Field(gt=0)
    medicine_prescription_id: int = Field(gt=0)

    note: Optional[str] = Field(default=None)


@admin_supplied_diagnose_router.post(
    "/supplied_diagnoses",
    response_model=SuppliedDiagnoses,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_supplied_diagnose_create(request: Request, dto: CreateSuppliedDiagnoseDto):
    query = (
        insert(SuppliedDiagnosesDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(SuppliedDiagnosesDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_supplied_diagnose = cursor.scalars().first()

    return SuppliedDiagnoses.model_validate(new_supplied_diagnose)
