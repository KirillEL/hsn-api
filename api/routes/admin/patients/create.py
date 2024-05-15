from datetime import date as tdate, date
from typing import Optional

from loguru import logger
from sqlalchemy.orm import joinedload

from api.decorators import HandleExceptions
from core.hsn.patient.commands.create import convert_to_patient_response
from core.hsn.patient.model import PatientResponse, BasePatientResponse
from shared.db.models import ContragentDBModel
from shared.db.models.patient import PatientDBModel
from shared.db.db_session import db_session, SessionContext
from .router import admin_patient_router
from core.hsn.patient import Patient
from api.exceptions import ExceptionResponseSchema
from sqlalchemy import select, insert
from pydantic import BaseModel, Field, ValidationError
from fastapi import Request
from utils import contragent_hasher
from shared.db.models.cabinet import CabinetDBModel
from api.exceptions import NotFoundException, InternalServerException, ValidationException
from ...protected.hsn.patient import CreatePatientRequestBody


class PatientCreateDto(CreatePatientRequestBody):
    cabinet_id: int = Field(gt=0)


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


@admin_patient_router.post(
    "/patients",
    response_model=BasePatientResponse,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
@HandleExceptions()
async def admin_patient_create(request: Request, dto: PatientCreateDto):
    logger.info(f'Начало создания пациента')
    patient_payload = dto.model_dump(
        exclude={'name', 'last_name', 'patronymic', 'birth_date', 'dod', 'cabinet_id', 'user_id'})
    contragent_payload = {
        'name': dto.name,
        'last_name': dto.last_name,
        'patronymic': dto.patronymic if dto.patronymic else "",
        'birth_date': dto.birth_date,
        'dod': dto.dod if dto.dod else None
    }
    new_contragent_id = await create_contragent(contragent_payload)
    logger.info(f'контрагент создан успешно!')
    patient_payload['location'] = str(patient_payload['location'])
    query = (
        insert(PatientDBModel)
        .values(
            author_id=request.user.id,
            cabinet_id=dto.cabinet_id,
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
    if not patient:
        raise NotFoundException(message="Пациент не найден!")
    patient_response = await convert_to_patient_response(patient)
    logger.info(f'patient_response: {patient_response}')
    return PatientResponse.model_validate(patient_response)
