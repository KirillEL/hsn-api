from datetime import date as tdate, datetime
from enum import Enum

from shared.db.queries import db_query_entity_by_id
from shared.redis import redis_service
from tg_api import tg_bot
from sqlalchemy import desc, asc, func, text, exc
from loguru import logger

from api.exceptions import InternalServerException
from ..helper import apply_ordering
from api.exceptions.base import ValidationErrorTelegramSendMessageSchema
from core.hsn.patient.commands.create import convert_to_patient_response
from shared.db.models import ContragentDBModel
from shared.db.models.cabinet import CabinetDBModel
from shared.db.models.patient import PatientDBModel
from shared.db.models.doctor import DoctorDBModel
from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import aliased, selectinload
from fastapi import Request
from ..model import DictPatientResponse


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


@SessionContext()
async def hsn_query_own_patients(
        request: Request,
        doctor_id: int,
        limit: int = None,
        offset: int = None,
        gender: str = None,
        full_name: str = None,
        location: str = None,
        columnKey: str = None,
        order: str = None
)-> DictPatientResponse:
    redis_key: str = "patients:all"

    cached_patients = await redis_service.get_data(redis_key)
    if cached_patients:
        return DictPatientResponse(
            data=cached_patients,
            total=len(cached_patients),
        )


    contragent_alias = aliased(ContragentDBModel)

    doctor_model: DoctorDBModel = await db_query_entity_by_id(DoctorDBModel, doctor_id)
    doctor_cabinet_id: int = doctor_model.cabinet_id

    query = (
        select(PatientDBModel)
        .where(
            PatientDBModel.is_deleted.is_(False),
            DoctorDBModel.id == doctor_id
        )
        .options(
            selectinload(PatientDBModel.cabinet)
                .selectinload(CabinetDBModel.doctors)
        )
        .options(
            selectinload(PatientDBModel.contragent)
        )
    )

    query_count = (
        select(func.count(PatientDBModel.id))
        .where(PatientDBModel.cabinet_id == doctor_cabinet_id)
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

    query = query.where(PatientDBModel.cabinet_id == doctor_cabinet_id)
    query = apply_ordering(query, PatientDBModel, columnKey, order)
    if columnKey == 'full_name':
        query = apply_ordering(query, full_name_expr, columnKey, order)

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    query = query.order_by(desc(PatientDBModel.created_at))

    total_count_result = await db_session.execute(query_count)
    total_count = total_count_result.scalar()


    cursor = await db_session.execute(query)
    patients = cursor.scalars().all()


    converted_patients = [await convert_to_patient_response(patient) for patient in patients]

    serialized_patients = [patient.to_dict() for patient in converted_patients]

    await redis_service.set_data_with_ttl(redis_key, serialized_patients, expire=300)


    return DictPatientResponse(
        data=converted_patients,
        total=total_count
    )
