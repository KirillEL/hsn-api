from datetime import date
from enum import Enum

from loguru import logger
from api.exceptions.base import NotFoundException
from core.hsn.patient.model import Patient
from shared.db.models import ContragentDBModel
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.patient import PatientDBModel
from shared.db.models.doctor import DoctorDBModel
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload

class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"

@SessionContext()
async def hsn_patient_own(current_user_id: int, limit: int = None, offset: int = None, age: int = None, gender: GenderType = None, dateBirth: date = None):
    query = (
        select(DoctorDBModel)
        .options(joinedload(DoctorDBModel.cabinet)
                 .joinedload(CabinetDBModel.patients)
                 .joinedload(PatientDBModel.contragent))
        .where(DoctorDBModel.user_id == current_user_id)
	)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if age is not None:
        query = query.where(PatientDBModel.age == age)

    if dateBirth is not None:
        query = query.where(ContragentDBModel.date_birth == dateBirth)


    cursor = await db_session.execute(query)
    doctor = cursor.scalars().first()
    doctor_patients = doctor.cabinet.patients

    if doctor_patients is None:
        raise NotFoundException(message="Пациенты не найдены")
    
    return [Patient.model_validate(d_p) for d_p in doctor_patients]