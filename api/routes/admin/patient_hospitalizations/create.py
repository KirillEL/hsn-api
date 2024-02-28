from datetime import datetime
from typing import Optional

from sqlalchemy import select, insert
from shared.db.db_session import SessionContext, db_session
from shared.db.models.patient_hospitalization import PatientHospitalizationsDBModel
from api.exceptions import ExceptionResponseSchema
from .router import admin_patient_hospitalization_router
from core.hsn.patient_hospitalization import PatientHospitalization
from pydantic import BaseModel, Field
from fastapi import Request


class PatientHospitalizationsCreateDto(BaseModel):
    patient_id: int = Field(gt=0)
    date_start: datetime
    date_end: datetime
    anamnes: Optional[str] = Field(None)



@admin_patient_hospitalization_router.post(
    "/patient_hospitalizations",
    response_model=PatientHospitalization,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_hospitalization_create(request: Request, dto: PatientHospitalizationsCreateDto):
    query = (
        insert(PatientHospitalizationsDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(PatientHospitalizationsDBModel)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_patient_hospitalization = cursor.scalars().first()

    return PatientHospitalization.model_validate(new_patient_hospitalization)