from core.hsn.patient.model import Contragent, PatientFlat, PatientResponse
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
    birth_date: tdate
    dod: Optional[tdate] = None
    location: str
    district: str
    address: str
    phone: int
    clinic: str
    patient_note: Optional[str] = None
    referring_doctor: Optional[str] = None
    referring_clinic_organization: Optional[str] = None
    disability: str
    lgota_drugs: str
    has_hospitalization: bool
    count_hospitalization: Optional[int] = None
    last_hospitalization_date: Optional[tdate] = None


async def convert_to_patient_response(patient) -> PatientResponse:
    decrypted_name = contragent_hasher.decrypt(patient.contragent.name)
    decrypted_last_name = contragent_hasher.decrypt(patient.contragent.last_name)
    decrypted_patronymic = contragent_hasher.decrypt(patient.contragent.patronymic)
    decrypted_birth_date = datetime.strptime(contragent_hasher.decrypt(patient.contragent.birth_date), "%Y-%m-%d").date()
    decrypted_dod = None
    if patient.contragent.dod is not None:
        decrypted_dod = datetime.strptime(contragent_hasher.decrypt(patient.contragent.dod), "%Y-%m-%d").date()

    full_name = f"{decrypted_last_name} {decrypted_name}"
    if decrypted_patronymic:
        full_name += f" {decrypted_patronymic}"

    today = tdate.today()
    age = today.year - decrypted_birth_date.year - (
                (today.month, today.day) < (decrypted_birth_date.month, decrypted_birth_date.day))

    patient_response = PatientResponse(
        id=patient.id,
        full_name=full_name,
        gender=patient.gender,
        age=age,
        birth_date=decrypted_birth_date,
        dod=decrypted_dod,
        location=patient.location,
        district=patient.district,
        address=patient.address,
        phone=patient.phone,
        clinic=patient.clinic,
        patient_note=patient.patient_note,
        referring_doctor=patient.referring_doctor,
        referring_clinic_organization=patient.referring_clinic_organization,
        disability=patient.disability,
        lgota_drugs=patient.lgota_drugs,
        has_hospitalization=patient.has_hospitalization,
        count_hospitalization=patient.count_hospitalization,
        last_hospitalization_date=patient.last_hospitalization_date
    )
    return patient_response

async def create_contragent(contragent_payload: dict[str, any]) -> int:
    hashed_payload = {
        'name': contragent_hasher.encrypt(contragent_payload['name']),
        'last_name': contragent_hasher.encrypt(contragent_payload['last_name']),
        'patronymic': contragent_hasher.encrypt(contragent_payload['patronymic']),
        'birth_date': contragent_hasher.encrypt(str(contragent_payload['birth_date'])),
        'dod': contragent_hasher.encrypt(str(contragent_payload['dod']))
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
    patient_payload = context.model_dump(exclude={'name', 'last_name', 'patronymic', 'birth_date', 'dod', 'cabinet_id', 'user_id'})
    contragent_payload = {
        'name': context.name,
        'last_name': context.last_name,
        'patronymic': context.patronymic,
        'birth_date': context.birth_date,
        'dod': context.dod
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


