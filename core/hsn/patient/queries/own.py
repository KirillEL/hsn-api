from datetime import date as tdate
from enum import Enum
from typing import Dict

from sqlalchemy import desc, asc, func
from loguru import logger

from api.decorators import HandleExceptions
from api.exceptions.base import NotFoundException
from core.hsn.patient.commands.create import convert_to_patient_response
from shared.db.models import ContragentDBModel
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.patient import PatientDBModel
from shared.db.models.doctor import DoctorDBModel
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased


class GenderType(str, Enum):
    MALE = "М"
    FEMALE = "Ж"


class LgotaDrugsType(str, Enum):
    NO = "нет"
    YES = "да"
    CCZ = "ссз"


class LocationType(Enum):
    NSO = "НСО"
    NSK = "Новосибирск"
    ANOTHER = "другое"


ContragentAlias = aliased(ContragentDBModel, name="contragents_1")


@HandleExceptions()
@SessionContext()
async def hsn_get_own_patients(current_user_id: int, limit: int = None, offset: int = None, full_name: str = None,
                               gender: str = None, columnKey: str = None, order: str = None):
    query = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.cabinet)
                 .joinedload(CabinetDBModel.doctors)
                 , joinedload(PatientDBModel.contragent))
        .where(DoctorDBModel.user_id == current_user_id)
    )
    logger.debug(f"Query: {query}")
    query_count = (
        select(func.count(PatientDBModel.id))
        .join(PatientDBModel.cabinet)
        .join(CabinetDBModel.doctors)
        .where(DoctorDBModel.user_id == current_user_id)
    )
    logger.debug(f"Query_count: {query_count}")
    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    logger.debug(f'gender: {gender}')
    if gender is not None:
        query = query.where(PatientDBModel.gender == gender[0])

    logger.debug(f'columnKey: {columnKey}')
    logger.debug(f'desc: {order}')
    if columnKey and hasattr(PatientDBModel, columnKey):
        column_attribute = getattr(PatientDBModel, columnKey)
        if order == "asc":
            query = query.order_by(asc(column_attribute))
        else:
            query = query.order_by(desc(column_attribute))

    if columnKey and hasattr(ContragentAlias, columnKey) and columnKey != 'id':
        column_attribute = getattr(ContragentAlias, columnKey)
        if order == "asc":
            query = query.order_by(asc(column_attribute))
        else:
            query = query.order_by(desc(column_attribute))

    total_count_result = await db_session.execute(query_count)
    total_count = total_count_result.scalar()
    logger.debug(f'get total_count: {total_count}')
    cursor = await db_session.execute(query)
    patients = cursor.unique().scalars().all()
    if len(patients) == 0:
        raise NotFoundException(message="Пациенты не найдены!")
    converted_patients = []
    for patient in patients:
        conv_patient = await convert_to_patient_response(patient)
        converted_patients.append(conv_patient)

    if full_name:
        filtered_patients = [patient for patient in converted_patients if
                             full_name[0].lower() in patient.full_name.lower()]
        total_count = len(filtered_patients)
    else:
        filtered_patients = converted_patients

    return {
        "data": filtered_patients,
        "total": total_count
    }
