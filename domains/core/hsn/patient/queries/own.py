from urllib.parse import unquote
from enum import Enum

from domains.shared.db.queries import db_query_entity_by_id
from domains.shared.redis import redis_service
from loguru import logger

from utils import contragent_hasher
from ..helper import apply_ordering
from domains.core.hsn.patient.commands.create import convert_to_patient_response
from domains.shared.db.models.cabinet import CabinetDBModel
from domains.shared.db.models.patient import PatientDBModel
from domains.shared.db.models.doctor import DoctorDBModel
from domains.shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import selectinload
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


async def check_query_params(
    redis_key: str,
    name: str,
    last_name: str,
    patronymic: str,
    birth: str,
    limit: int,
    offset: int,
) -> str:
    if name:
        redis_key += f":name:{name}"

    if last_name:
        redis_key += f":last_name:{last_name}"

    if patronymic:
        redis_key += f":patronymic:{patronymic}"

    if birth:
        redis_key += f":birth:{birth}"

    if limit:
        redis_key += f":limit:{limit}"

    if offset:
        redis_key += f":offset:{offset}"

    return redis_key


@SessionContext()
async def hsn_query_own_patients(
    request: Request,
    doctor_id: int,
    limit: int = None,
    offset: int = None,
    name: str = None,
    last_name: str = None,
    patronymic: str = None,
    birth: str = None,
    columnKey: str = None,
    order: str = None,
) -> DictPatientResponse:
    doctor_model: DoctorDBModel = await db_query_entity_by_id(DoctorDBModel, doctor_id)
    if name:
        name = unquote(name)

    if last_name:
        last_name = unquote(last_name)

    if patronymic:
        patronymic = unquote(patronymic)

    redis_key: str = f"patients:doctor:{doctor_id}"

    redis_key = await check_query_params(
        redis_key, name, last_name, patronymic, birth, limit, offset
    )

    cached_patients = await redis_service.get_data(redis_key)
    if cached_patients:
        return DictPatientResponse(
            data=cached_patients["data"],
            total=cached_patients["total"],
        )

    query = (
        select(PatientDBModel)
        .options(
            selectinload(PatientDBModel.cabinet).selectinload(CabinetDBModel.doctors),
            selectinload(PatientDBModel.contragent),
        )
        .where(PatientDBModel.is_deleted.is_(False))
        .where(PatientDBModel.cabinet_id == doctor_model.cabinet_id)
    )

    query = apply_ordering(query, PatientDBModel, columnKey, order)

    logger.debug(f"query: {query}")

    cursor = await db_session.execute(query)
    patients = cursor.scalars().all()

    filtered_patients = []
    for patient in patients:
        contragent = patient.contragent

        decrypted_name = (
            contragent_hasher.decrypt(contragent.name) if contragent.name else None
        )
        decrypted_last_name = (
            contragent_hasher.decrypt(contragent.last_name)
            if contragent.last_name
            else None
        )
        decrypted_patronymic = (
            contragent_hasher.decrypt(contragent.patronymic)
            if contragent.patronymic
            else None
        )
        decrypted_birth = (
            contragent_hasher.decrypt(contragent.birth_date)
            if contragent.birth_date
            else None
        )

        if (
            (not name or (decrypted_name and name.lower() in decrypted_name.lower()))
            and (
                not last_name
                or (
                    decrypted_last_name
                    and last_name.lower() in decrypted_last_name.lower()
                )
            )
            and (
                not patronymic
                or (
                    decrypted_patronymic
                    and patronymic.lower() in decrypted_patronymic.lower()
                )
            )
            and (not birth or (decrypted_birth and birth == decrypted_birth))
        ):
            filtered_patients.append(patient)

    total_count = len(filtered_patients)

    paginated_patients = filtered_patients

    if offset is not None:
        paginated_patients = filtered_patients[offset:]

    if limit is not None:
        paginated_patients = paginated_patients[:limit]

    converted_patients = [
        await convert_to_patient_response(patient) for patient in paginated_patients
    ]
    serialized_patients = [patient.to_dict() for patient in converted_patients]

    await redis_service.set_data_with_ttl(
        redis_key,
        {"data": serialized_patients, "total": total_count},
        expire=300,
    )

    return DictPatientResponse(data=converted_patients, total=total_count)
