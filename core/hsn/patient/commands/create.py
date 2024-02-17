from shared.db.db_session import db_session, SessionContext
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import insert
from shared.db.models.contragent import ContragentDBModel
from shared.db.models.patient import PatientDBModel
from core.hsn.patient import Patient
from datetime import date
from core.user.queries.me import hsn_user_get_me
from loguru import logger
from utils import cipher


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
    # cabinet_id: int

    phone_number: int
    snils: str
    address: str
    mis_number: int
    date_birth: date
    relative_phone_number: int
    parent: str
    date_dead: Optional[date] = None


@SessionContext()
async def hsn_patient_create(context: HsnPatientCreateContext):
    # 1
    user = await hsn_user_get_me(context.user_id)

    patient_payload = context.model_dump(
        exclude={'phone_number', 'snils', 'address', 'mis_number', 'date_birth', 'relative_phone_number', 'parent',
                 'date_dead', 'user_id'})

    query_contragent = (
        insert(ContragentDBModel)
        .values(
            phone_number=cipher.encrypt(str(context.phone_number)).decode('utf-8'),
            snils=cipher.encrypt(context.snils).decode('utf-8'),
            address=cipher.encrypt(context.address).decode('utf-8'),
            mis_number=cipher.encrypt(str(context.mis_number)).decode('utf-8'),
            date_birth=cipher.encrypt(str(context.date_birth)).decode('utf-8'),
            relative_phone_number=cipher.encrypt(str(context.relative_phone_number)).decode('utf-8'),
            parent=cipher.encrypt(context.parent).decode('utf-8'),
            date_dead=cipher.encrypt(str(context.date_dead)).decode('utf-8'),
            author_id=user.id
        )
        .returning(ContragentDBModel.id)
    )
    logger.debug(f"query_contragent={query_contragent}")
    cursor = await db_session.execute(query_contragent)
    await db_session.commit()
    contragent_id = cursor.scalars().first()
    logger.debug(f"contragent_id={contragent_id}")

    # 2
    query_patient = (
        insert(PatientDBModel)
        .values(
            **patient_payload,
            contragent_id=contragent_id,
            author_id=user.id,
            cabinet_id=user.doctor.cabinet_id
        )
        .returning(PatientDBModel)
    )
    logger.debug(f"query_patient={query_patient}")
    cursor_2 = await db_session.execute(query_patient)
    await db_session.commit()
    new_patient = cursor_2.scalars().first()
    logger.debug(f"new_patient={new_patient}")
    return Patient.model_validate(new_patient)
