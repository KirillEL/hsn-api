from datetime import date as tdate
from typing import Optional
from sqlalchemy.orm import joinedload
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


class PatientCreateDto(BaseModel):
    name: str = Field(None, max_length=100)
    last_name: str = Field(None, max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    age: int = Field(None, gt=0)
    gender: str = Field("")
    height: int = Field(None, gt=0)
    date_setup_diagnose: tdate = Field(...)
    lgota_drugs: str = Field("")
    note: str = Field(None, max_length=5000)
    cabinet_id: int = Field(None, gt=0)

    phone_number: str = Field(None)
    snils: str = Field(None, max_length=16)
    address: str = Field(None, max_length=1000)
    mis_number: str = Field(None)
    date_birth: str = Field(...)
    relative_phone_number: Optional[str] = Field(...)
    parent: Optional[str] = Field(...)
    date_dead: Optional[tdate] = Field(None)


async def create_contragent_and_return_id(contragent_dto: dict[str, any]) -> int | None:
    try:
        query = (
            insert(ContragentDBModel)
            .values(
                phone_number=contragent_hasher.encrypt(value=contragent_dto.get('phone_number')),
                snils=contragent_hasher.encrypt(value=contragent_dto.get('snils')),
                address=contragent_hasher.encrypt(value=contragent_dto.get('address')),
                mis_number=contragent_hasher.encrypt(value=contragent_dto.get('mis_number')),
                date_birth=contragent_hasher.encrypt(value=contragent_dto.get('date_birth')),
                relative_phone_number=contragent_hasher.encrypt(value=contragent_dto.get('relative_phone_number')) if contragent_dto.get('relative_phone_number') is not None else "",
                parent=contragent_hasher.encrypt(value=contragent_dto.get('parent')) if contragent_dto.get('parent') is not None else "",
                date_dead=contragent_hasher.encrypt(value=contragent_dto.get('date_dead') if contragent_dto.get('date_dead') is not None else "")
            )
            .returning(ContragentDBModel.id)
        )
        cursor = await db_session.execute(query)
        await db_session.commit()
        new_contragent_id = cursor.scalar()
        return new_contragent_id
    except Exception as e:
        await db_session.rollback()
        raise e


async def check_cabinet_exists(cabinet_id: int) -> None:
    query = (
        select(CabinetDBModel)
        .where(CabinetDBModel.id == cabinet_id, CabinetDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    cabinet = cursor.scalars().first()
    if cabinet is None:
        raise NotFoundException(message="Кабинет не найден !")


async def create_patient(patient_dto: dict[str, any], contragent_id: int, author_id: int) -> None | int:
    try:
        await check_cabinet_exists(patient_dto.get('cabinet_id'))
        query = (
            insert(PatientDBModel)
            .values(
                **patient_dto,
                contragent_id=contragent_id,
                author_id=author_id
            )
            .returning(PatientDBModel.id)
        )
        cursor = await db_session.execute(query)
        await db_session.commit()
        new_patient_id = cursor.scalar()
        return new_patient_id
    except Exception as e:
        await db_session.rollback()
        raise e


@admin_patient_router.post(
    "/patients",
    response_model=Patient,
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_patient_create(request: Request, dto: PatientCreateDto):
    contragent_dto = dto.model_dump(exclude={
        'name',
        'last_name',
        'patronymic',
        'age',
        'gender',
        'height',
        'date_setup_diagnose',
        'lgota_drugs',
        'note',
        'last_hospitalization_id',
        'cabinet_id'
    })
    patient_dto = dto.model_dump(exclude={
        "phone_number",
        "snils",
        "address",
        "mis_number",
        "date_birth",
        "relative_phone_number",
        "parent",
        "date_dead",
    })
    try:
        new_contragent_id = await create_contragent_and_return_id(contragent_dto=contragent_dto)
        new_patient_id = await create_patient(patient_dto=patient_dto, contragent_id=new_contragent_id,
                                              author_id=request.user.id)

        query_get_new_patient = (
            select(PatientDBModel)
            .options(joinedload(PatientDBModel.contragent))
            .where(PatientDBModel.id == new_patient_id)
        )
        cursor = await db_session.execute(query_get_new_patient)
        new_patient = cursor.scalars().first()

        new_patient.contragent.phone_number = contragent_hasher.decrypt(new_patient.contragent.phone_number)
        new_patient.contragent.snils = contragent_hasher.decrypt(new_patient.contragent.snils)
        new_patient.contragent.address = contragent_hasher.decrypt(new_patient.contragent.address)
        new_patient.contragent.mis_number = contragent_hasher.decrypt(new_patient.contragent.mis_number)
        new_patient.contragent.date_birth = contragent_hasher.decrypt(new_patient.contragent.date_birth)
        new_patient.contragent.relative_phone_number = contragent_hasher.decrypt(
            new_patient.contragent.relative_phone_number)
        new_patient.contragent.parent = contragent_hasher.decrypt(new_patient.contragent.parent)
        new_patient.contragent.date_dead = contragent_hasher.decrypt(new_patient.contragent.date_dead)

        return Patient.model_validate(new_patient)
    except ValidationError as ve:
        raise ValidationException(message=str(ve))
    except Exception as e:
        raise InternalServerException(message=str(e))

