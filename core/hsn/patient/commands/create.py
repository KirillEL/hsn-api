from core.hsn.patient.model import Contragent
from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import insert, select
from shared.db.models.contragent import ContragentDBModel
from shared.db.models.patient import PatientDBModel
from core.hsn.patient import Patient
from datetime import date
from core.user.queries.me import hsn_user_get_me
from loguru import logger
from utils import contragent_hasher
from api.exceptions import BadRequestException
from sqlalchemy.orm import joinedload


class HsnPatientCreateContext(BaseModel):
    user_id: int

    name: str
    last_name: str
    patronymic: Optional[str]
    age: int
    gender: str
    height: int
    main_diagnose: str
    disability: str
    date_setup_diagnose: date
    school_hsn_date: date
    have_hospitalization: bool
    count_hospitalizations: int
    lgota_drugs: str
    last_hospitalization_id: Optional[int] = None
    note: str
    has_chronic_heart: bool = False
    classification_func_classes: str
    has_stenocardia: bool = False
    has_arteria_hypertension: bool = False
    arteria_hypertension_age: int

    phone_number: int
    snils: str
    address: str
    mis_number: int
    date_birth: date
    relative_phone_number: int
    parent: str
    date_dead: Optional[date] = None


class ContragentContext(BaseModel):
    phone_number: str  # int
    snils: str
    address: str
    mis_number: str  # int
    date_birth: str  # date
    relative_phone_number: str  # int
    parent: str
    date_dead: Optional[str] = None  # date


async def create_contragent(contragent_payload: ContragentContext, author_id: int) -> int:
    try:
        query = (
            insert(ContragentDBModel)
            .values(
                **contragent_payload,
                author_id=author_id
            )
            .returning(ContragentDBModel.id)
        )
        logger.debug(f'contragent_query: {query}')
        cursor = await db_session.execute(query)
        await db_session.commit()
        contragent_id = cursor.scalars().first()
        logger.debug(f'new_contragent: {contragent_id}')
        return contragent_id
    except Exception as e:
        await db_session.rollback()
        raise BadRequestException(message=str(e))


async def get_patient_by_id(patient_id: int):
    try:
        query = (
            select(PatientDBModel)
            .options(joinedload(PatientDBModel.contragent))
            .where(PatientDBModel.id == patient_id)
        )
        cursor = await db_session.execute(query)
        await db_session.commit()
        patient = cursor.scalars().first()
        return patient
    except Exception as e:
        await db_session.rollback()
        raise BadRequestException(message=str(e))


async def create_patient_and_get_by_id(patient_payload: dict, contragent_id: int, author_id: int, cabinet_id: int):
    try:
        query = (
            insert(PatientDBModel)
            .values(
                **patient_payload,
                author_id=author_id,
                contragent_id=contragent_id,
                cabinet_id=cabinet_id
            )
            .returning(PatientDBModel.id)
        )
        logger.debug(f'patient_query: {query}')
        cursor = await db_session.execute(query)
        await db_session.commit()
        new_patient_id = cursor.scalars().first()
        new_patient = await get_patient_by_id(new_patient_id)
        return new_patient
    except Exception as e:
        await db_session.rollback()
        raise BadRequestException(message=str(e))


@SessionContext()
async def hsn_patient_create(context: HsnPatientCreateContext):
    user = await hsn_user_get_me(context.user_id)

    patient_payload = context.model_dump(
        exclude={'phone_number', 'snils', 'address', 'mis_number', 'date_birth', 'relative_phone_number', 'parent',
                 'date_dead', 'user_id'})

    contragent_payload = ContragentContext(
        phone_number=contragent_hasher.encrypt(value=str(context.phone_number)),
        snils=contragent_hasher.encrypt(value=context.snils),
        address=contragent_hasher.encrypt(value=context.address),
        mis_number=contragent_hasher.encrypt(value=str(context.mis_number)),
        date_birth=contragent_hasher.encrypt(value=context.date_birth.isoformat()),
        relative_phone_number=contragent_hasher.encrypt(value=str(context.relative_phone_number)),
        parent=contragent_hasher.encrypt(value=context.parent),
        date_dead=contragent_hasher.encrypt(value=context.date_dead.isoformat()) if context.date_dead else None
    ).dict()

    contragent_id = await create_contragent(contragent_payload=contragent_payload, author_id=user.id)
    new_patient = await create_patient_and_get_by_id(patient_payload=patient_payload, contragent_id=contragent_id,
                                                     author_id=user.id,
                                                     cabinet_id=user.doctor.cabinet_id)
    return Patient.from_orm(new_patient)
