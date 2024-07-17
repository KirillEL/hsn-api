from typing import Optional

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import update, select

from api.exceptions import NotFoundException
from core.hsn.doctor.schemas import UserAndDoctor
from shared.db import Transaction, session
from shared.db.models import UserDBModel, CabinetDBModel
from shared.db.transaction import Propagation
from utils import PasswordHasher, contragent_hasher


class UserDoctorUpdateContext(BaseModel):
    user_id: int
    login: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None
    cabinet_id: Optional[int] = None


@Transaction(propagation=Propagation.REQUIRED)
async def user_command_update(context: UserDoctorUpdateContext):
    payload = context.model_dump(exclude_none=True)
    logger.debug(f'payload: {payload}')
    query_get_user = (
        select(UserDBModel)
        .where(UserDBModel.id == context.user_id)
    )
    cursor = await session.execute(query_get_user)
    user = cursor.scalars().first()
    if not user:
        raise NotFoundException(message="Пользователь не найден!")

    if payload.get("login"):
        user.login = payload.get("login")

    if payload.get("password"):
        hashed_password = PasswordHasher.hash_password(payload.get("password"))
        user.password = hashed_password

    doctor = user.doctor
    if payload.get("name"):
        doctor.name = payload.get("name")

    if payload.get("last_name"):
        doctor.last_name = payload.get("last_name")

    if context.patronymic is not None:
        doctor.patronymic = context.patronymic
    if context.phone_number is not None:
        doctor.phone_number = context.phone_number

    if context.cabinet_id is not None:
        cabinet = await session.get(CabinetDBModel, context.cabinet_id)
        if not cabinet:
            raise NotFoundException(message="Кабинет не найден!")
        doctor.cabinet_id = context.cabinet_id

    return UserAndDoctor.model_validate(user)

