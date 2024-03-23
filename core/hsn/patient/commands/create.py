from core.hsn.patient.model import Contragent, PatientFlat
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from sqlalchemy import insert, select
from shared.db.models.contragent import ContragentDBModel
from shared.db.models.patient import PatientDBModel
from core.hsn.patient import Patient
from datetime import date as tdate, datetime
from core.user.queries.me import hsn_user_get_me
from loguru import logger
from utils.hash_helper import contragent_hasher
from api.exceptions import BadRequestException, ValidationException
from sqlalchemy.orm import joinedload


class HsnPatientCreateContext(BaseModel):
    user_id: int

    name: str
    last_name: str
    patronymic: Optional[str] = None
    age: int
    gender: str
    height: int
    date_setup_diagnose: datetime
    lgota_drugs: str
    note: Optional[str] = None
    cabinet_id: int

    phone_number: int
    snils: str
    address: str
    mis_number: int
    date_birth: tdate
    relative_phone_number: Optional[int] = None
    parent: Optional[str] = None
    date_dead: Optional[tdate] = None


async def create_contragent_and_get_id(contragent_payload: dict[str, any]):
    try:
        hashed_payload = {key: contragent_hasher.encrypt(str(value)) for key, value in contragent_payload.items()}

        query = (
            insert(ContragentDBModel)
            .values(**hashed_payload)
            .returning(ContragentDBModel.id)
        )
        cursor = await db_session.execute(query)
        await db_session.commit()
        contragent_id = cursor.scalar()
        return contragent_id
    except Exception as e:
        logger.error(f'Ошибка при создании контрагента: {e}')
        raise


async def create_patient(patient_payload: dict[str, any], contragent_id: int, author_id: int):
    try:
        query = (
            insert(PatientDBModel)
            .values(
                **patient_payload,
                author_id=author_id,
                contragent_id=contragent_id
            )
            .returning(PatientDBModel.id)
        )
        cursor = await db_session.execute(query)
        new_patient_id = cursor.scalar()
        await db_session.commit()

        query_get = (
            select(PatientDBModel)
            .options(joinedload(PatientDBModel.contragent), joinedload(PatientDBModel.cabinet))
            .where(PatientDBModel.id == new_patient_id)
        )
        cursor = await db_session.execute(query_get)
        new_patient = cursor.scalars().first()
        return new_patient
    except Exception as e:
        logger.error(f'Ошибка при создании пациента: {e}')
        raise


@SessionContext()
async def hsn_patient_create(context: HsnPatientCreateContext):
    logger.info('Начало создания пациента')
    try:
        contragent_payload = context.model_dump(exclude={
            'name',
            'last_name',
            'patronymic',
            'gender',
            'height',
            'age',
            'date_setup_diagnose',
            'lgota_drugs',
            'user_id',
            'cabinet_id',
            'note'
        })
        patient_payload = context.model_dump(
            exclude={
                'phone_number',
                'snils',
                'address',
                'mis_number',
                'date_birth',
                'relative_phone_number',
                'parent',
                'date_dead',
                'user_id'
            }
        )
        contragent_id = await create_contragent_and_get_id(contragent_payload)
        new_patient = await create_patient(patient_payload, contragent_id, context.user_id)
        return PatientFlat.model_validate(new_patient)
    except ValidationError as ve:
        logger.error(f'Ошибка валидации: {ve}')
        raise ValidationException()
    except Exception as e:
        logger.error(f'Ошибка при создании пациента: {e}')
        raise BadRequestException()
