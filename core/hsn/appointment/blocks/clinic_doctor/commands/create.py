from typing import Optional

from sqlalchemy import insert
from shared.db.db_session import db_session, SessionContext
from shared.db.models.appointment.blocks.block_clinic_doctor import AppointmentBlockClinicDoctorDBModel
from pydantic import BaseModel
from datetime import date as tdate

class HsnAppointmentBlockClinicDoctorCreateContext(BaseModel):
    reffering_doctor: Optional[str] = None
    reffering_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: Optional[bool] = False
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[tdate] = None

@SessionContext()
async def hsn_appointment_block_clinic_doctor_create(context: HsnAppointmentBlockClinicDoctorCreateContext):
    query = (
        insert(AppointmentBlockClinicDoctorDBModel)
        .values(**context.model_dump())
        .returning(AppointmentBlockClinicDoctorDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_block_clinic_doctor_id = cursor.scalar()
    return new_block_clinic_doctor_id