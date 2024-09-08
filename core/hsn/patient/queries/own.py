from datetime import date as tdate
from enum import Enum
from typing import Dict

from sqlalchemy import desc, asc, func, text
from loguru import logger
from ..helper import apply_ordering
from api.decorators import HandleExceptions
from api.exceptions.base import NotFoundException
from core.hsn.patient.commands.create import convert_to_patient_response
from shared.db.models import ContragentDBModel
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.patient import PatientDBModel
from shared.db.models.doctor import DoctorDBModel
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased, selectinload


class GenderType(str, Enum):
    MALE = "М"
    FEMALE = "Ж"


class LgotaDrugsType(str, Enum):
    NO = "нет"
    YES = "да"
    CCZ = "ССЗ"


class LocationType(Enum):
    NSO = "НСО"
    NSK = "Новосибирск"
    ANOTHER = "другое"


@HandleExceptions()
@SessionContext()
async def hsn_get_own_patients(doctor_id: int,
                               limit: int = None,
                               offset: int = None,
                               gender: str = None,
                               full_name: str = None,
                               location: str = None,
                               columnKey: str = None,
                               order: str = None):
    contragent_alias = aliased(ContragentDBModel)

    # Основной запрос
    query = (
        select(PatientDBModel)
        .options(selectinload(PatientDBModel.cabinet).selectinload(CabinetDBModel.doctors),
                 selectinload(PatientDBModel.contragent))
        .join(contragent_alias, PatientDBModel.contragent_id == contragent_alias.id)
        .where(DoctorDBModel.id == doctor_id)
    )

    query_count = (
        select(func.count(PatientDBModel.id))
        .join(contragent_alias, PatientDBModel.contragent_id == contragent_alias.id)
        .where(DoctorDBModel.id == doctor_id)
    )

    if gender:
        query = query.where(PatientDBModel.gender == gender[0])
        query_count = query_count.where(PatientDBModel.gender == gender[0])

    if location:
        query = query.where(PatientDBModel.location == location[0])
        query_count = query_count.where(PatientDBModel.location == location[0])

    if full_name:
        full_name_expr = func.concat(contragent_alias.last_name, ' ', contragent_alias.name, ' ',
                                     contragent_alias.patronymic)
        query = query.where(full_name_expr.ilike(f'%{full_name[0]}%'))
        query_count = query_count.where(full_name_expr.ilike(f'%{full_name[0]}%'))

    query = apply_ordering(query, PatientDBModel, columnKey, order)
    if columnKey == 'full_name':
        query = apply_ordering(query, full_name_expr, columnKey, order)

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    total_count_result = await db_session.execute(query_count)
    total_count = total_count_result.scalar()

    cursor = await db_session.execute(query)
    patients = cursor.unique().scalars().all()

    converted_patients = [await convert_to_patient_response(patient) for patient in patients]

    return {
        "data": converted_patients,
        "total": total_count
    }
