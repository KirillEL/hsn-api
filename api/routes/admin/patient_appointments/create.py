from datetime import datetime
from datetime import date as tdate
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
    cabinet_id: Optional[int] = Field(..., gt=0)
    date: datetime = Field(None)
    date_next: Optional[tdate]

    imt: float = Field(None)

    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)

    disability: str = Field(None)
    school_hsn_date: Optional[tdate]
    classification_func_classes: Optional[str] = Field(None)
    classification_adjacent_release: Optional[str] = Field(None)
    classification_nc_stage: Optional[str] = Field(None)

    has_stenocardia_napryzenya: bool = Field(False)
    has_myocardial_infraction: bool = Field(False)
    has_arteria_hypertension: bool = Field(False)

    arteria_hypertension_age: Optional[int] = Field(None, gt=0)

    fv_lg: int = Field(..., gt=0)
    main_diagnose: str = Field(None)
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

    note_complaints: Optional[str] = Field(None, max_length=1000)
    note_clinical: Optional[str] = Field(None, max_length=1000)
    note_ekg: Optional[str] = Field(None, max_length=1000)

    date_ekg: Optional[tdate]
    date_echo_ekg: Optional[tdate]
    fraction_out: float = Field(None, gt=0)
    sdla: float = Field(None, gt=0)

    nt_pro_bnp: float = Field(None)
    date_nt_pro_bnp: Optional[tdate]
    microalbumuria: float = Field(None, gt=0)
    date_microalbumuria: Optional[tdate] = Field(None)


@admin_patient_appointment_router.post(
    "/patient_appointments",
    response_model=PatientAppointment,
    responses={'400': {'model': ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_appointment_create(request: Request, dto: CreatePatientAppointmentDto):
    try:
        query = (
            insert(PatientAppointmentsDBModel)
            .values(
                **dto.dict(),
                author_id=request.user.id
            )
            .returning(PatientAppointmentsDBModel)
        )
        cursor = await db_session.execute(query)

        new_patient_appointment = cursor.scalars().first()

        validated_patient_appointment = PatientAppointment.model_validate(new_patient_appointment)
        await db_session.commit()
        return validated_patient_appointment
    except Exception as e:
        await db_session.rollback()
        raise e
