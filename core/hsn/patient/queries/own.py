from datetime import date
from enum import Enum
from sqlalchemy import desc, asc, func
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
from datetime import datetime
from utils.hash_helper import contragent_hasher


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"


@SessionContext()
async def hsn_get_own_patients(current_user_id: int, limit: int = None, offset: int = None, age: int = None,
                               gender: GenderType = None, dateBirth: date = None):
    query = (
        select(DoctorDBModel)
        .options(joinedload(DoctorDBModel.cabinet)
                 .joinedload(CabinetDBModel.patients)
                 .joinedload(PatientDBModel.contragent),
                 joinedload(DoctorDBModel.cabinet)
                 .joinedload(CabinetDBModel.patients)
                 .joinedload(PatientDBModel.cabinet)
                 )
        .where(DoctorDBModel.user_id == current_user_id)
    )

    query_count = (
        select(func.count(PatientDBModel.id))
        .join(PatientDBModel.cabinet)
        .join(CabinetDBModel.doctors)
        .where(DoctorDBModel.user_id == current_user_id)
    )

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if age is not None:
        query = query.where(PatientDBModel.age == age)
        query_count = query_count.where(PatientDBModel.age == age)

    if gender is not None:
        query = query.where(PatientDBModel.gender == gender.value)
        query_count = query_count.where(PatientDBModel.gender == gender.value)

    if dateBirth is not None:
        pass

    total_count_result = await db_session.execute(query_count)
    total_count = total_count_result.scalar()

    cursor = await db_session.execute(query)
    doctor = cursor.scalars().first()
    if doctor is None:
        raise NotFoundException(message="Пациенты не найдены!")
    doctor_patients = doctor.cabinet.patients
    for patient in doctor_patients:
        patient.contragent.phone_number = contragent_hasher.decrypt(patient.contragent.phone_number)
        patient.contragent.snils = contragent_hasher.decrypt(patient.contragent.snils)
        patient.contragent.address = contragent_hasher.decrypt(patient.contragent.address)
        patient.contragent.mis_number = contragent_hasher.decrypt(patient.contragent.mis_number)
        patient.contragent.date_birth = contragent_hasher.decrypt(patient.contragent.date_birth)
        patient.contragent.relative_phone_number = contragent_hasher.decrypt(patient.contragent.relative_phone_number)
        patient.contragent.parent = contragent_hasher.decrypt(patient.contragent.parent)
        patient.contragent.date_dead = contragent_hasher.decrypt(patient.contragent.date_dead)

    data = [Patient.model_validate(d_p) for d_p in doctor_patients]
    return {
        "data": data,
        "total": total_count
    }
