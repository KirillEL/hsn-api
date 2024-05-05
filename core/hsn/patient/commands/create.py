from core.hsn.patient.model import Contragent, PatientFlat, PatientResponse, PatientResponseWithoutFullName
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
    user_id: int = Field(gt=0)
    cabinet_id: int = Field(gt=0)

    name: str
    last_name: str
    patronymic: Optional[str] = None
    gender: str
    birth_date: str
    dod: Optional[str] = None
    location: str
    district: str
    address: str
    phone: str
    clinic: str
    patient_note: Optional[str] = None



async def convert_to_patient_response(patient, type: str = "full_name") ->  PatientResponse | PatientResponseWithoutFullName:
    decrypted_name = contragent_hasher.decrypt(patient.contragent.name)
    decrypted_last_name = contragent_hasher.decrypt(patient.contragent.last_name)
    decrypted_patronymic = contragent_hasher.decrypt(patient.contragent.patronymic)

    decrypted_birth_date_str = contragent_hasher.decrypt(patient.contragent.birth_date)
    decrypted_birth_date = datetime.strptime(decrypted_birth_date_str, "%d.%m.%Y").strftime("%d.%m.%Y")

    decrypted_dod = None
    if patient.contragent.dod:
        decrypted_dod_str = contragent_hasher.decrypt(patient.contragent.dod)
        if decrypted_dod_str:  # Ensure the string is not empty
            decrypted_dod = datetime.strptime(decrypted_dod_str, "%d.%m.%Y").strftime("%d.%m.%Y")

    full_name = f"{decrypted_last_name} {decrypted_name}"
    if decrypted_patronymic:
        full_name += f" {decrypted_patronymic}"

    birth_date_obj = datetime.strptime(decrypted_birth_date, "%d.%m.%Y").date()
    today = tdate.today()
    age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))

    if type == "full_name":
        patient_response = PatientResponse(
            id=patient.id,
            full_name=full_name,
            gender=patient.gender,
            age=age,
            birth_date=decrypted_birth_date,  # Already formatted
            dod=decrypted_dod,  # Already formatted, if exists
            location=patient.location,
            district=patient.district,
            address=patient.address,
            phone=patient.phone,
            clinic=patient.clinic,
            patient_note=patient.patient_note,
        )
        return patient_response
    else:
        patient_response = PatientResponseWithoutFullName(
            id=patient.id,
            name=decrypted_name,
            last_name=decrypted_last_name,
            patronymic=decrypted_patronymic,
            gender=patient.gender,
            age=age,
            birth_date=decrypted_birth_date,  # Already formatted
            dod=decrypted_dod,  # Already formatted, if exists
            location=patient.location,
            district=patient.district,
            address=patient.address,
            phone=patient.phone,
            clinic=patient.clinic,
            patient_note=patient.patient_note,
        )
        return patient_response


async def create_contragent(contragent_payload: dict[str, any]) -> int:
    hashed_payload = {
        'name': contragent_hasher.encrypt(contragent_payload['name']),
        'last_name': contragent_hasher.encrypt(contragent_payload['last_name']),
        'patronymic': contragent_hasher.encrypt(contragent_payload['patronymic']),
        'birth_date': contragent_hasher.encrypt(str(contragent_payload['birth_date'])),
        'dod': contragent_hasher.encrypt(str(contragent_payload['dod'])) if contragent_payload['dod'] else None
    }
    query = (
        insert(ContragentDBModel)
        .values(**hashed_payload)
        .returning(ContragentDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    new_contragent_id = cursor.scalar()
    return new_contragent_id


@SessionContext()
async def hsn_patient_create(context: HsnPatientCreateContext):
    logger.info(f'Начало создания пациента')
    patient_payload = context.model_dump(
        exclude={'name', 'last_name', 'patronymic', 'birth_date', 'dod', 'cabinet_id', 'user_id'})
    contragent_payload = {
        'name': context.name,
        'last_name': context.last_name,
        'patronymic': context.patronymic if context.patronymic else "",
        'birth_date': context.birth_date,
        'dod': context.dod if context.dod else None
    }
    new_contragent_id = await create_contragent(contragent_payload)
    logger.info(f'контрагент создан успешно!')

    query = (
        insert(PatientDBModel)
        .values(
            author_id=context.user_id,
            cabinet_id=context.cabinet_id,
            **patient_payload,
            contragent_id=new_contragent_id
        )
        .returning(PatientDBModel.id)
    )
    cursor = await db_session.execute(query)
    await db_session.commit()
    patient_id = cursor.scalar()
    query_get = (
        select(PatientDBModel)
        .options(joinedload(PatientDBModel.contragent))
        .where(PatientDBModel.id == patient_id)
    )
    cursor = await db_session.execute(query_get)
    patient = cursor.scalars().first()
    patient_response = await convert_to_patient_response(patient)
    logger.info(f'patient_response: {patient_response}')
    return PatientResponse.model_validate(patient_response)
