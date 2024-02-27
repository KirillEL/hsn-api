from datetime import datetime
from typing import Optional

from sqlalchemy import select, insert
from fastapi import Request
from .router import admin_patient_appointment_router
from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient_appointment import PatientAppointmentsDBModel
from core.hsn.patient_appointment import PatientAppointment
from api.exceptions import ExceptionResponseSchema
from pydantic import BaseModel, Field


class CreatePatientAppointmentDto(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    cabinet_id: int = Field(..., gt=0)
    date: datetime
    date_next: Optional[datetime] = Field(None)
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    fv_lg: int = Field(..., gt=0)
    main_diagnose: str
    sistol_ad: float = Field(..., gt=0)
    diastal_ad: float = Field(..., gt=0)
    hss: int = Field(..., gt=0)
    mit: Optional[float] = Field(None)
    has_fatigue: bool = Field(False)
    has_dyspnea: bool = Field(False)
    has_swelling_legs: bool = Field(False)
    has_weakness: bool = Field(False)
    has_orthopnea: bool = Field(False)
    has_heartbeat: bool = Field(True)
    note: Optional[str] = Field(None)


@admin_patient_appointment_router.post(
    "/patient_appointments",
    response_model=PatientAppointment,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_appointment_create(request: Request, dto: CreatePatientAppointmentDto):
    query = (
        insert(PatientAppointmentsDBModel)
        .values(
            **dto,
            author_id=request.user.id
        )
        .returning(PatientAppointmentsDBModel)
    )
    cursor = await db_session.execute(query)
    new_patient_appointment = cursor.scalars().first()

    return PatientAppointment.model_validate(new_patient_appointment)
