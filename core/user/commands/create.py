from typing import Optional

from loguru import logger
from api.exceptions.base import InternalServerException, NotFoundException, ValidationException
from sqlalchemy.orm import joinedload

from shared.db import Transaction
from shared.db.db_session import session
from pydantic import BaseModel, Field, ValidationError
from core.hsn.doctor.schemas import UserAndDoctor
from sqlalchemy import insert, select

from shared.db.models import CabinetDBModel
from shared.db.models.role import RoleDBModel
from shared.db.models.user import UserDBModel
from shared.db.models.doctor import DoctorDBModel
from shared.db.models.user_role import UserRoleDBModel
from shared.db.transaction import Propagation
from utils import PasswordHasher


class UserDoctorCreateContext(BaseModel):
    login: str = Field(None, max_length=25)
    password: str = Field(None, min_length=6)
    name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    patronymic: Optional[str] = Field(None, max_length=100)
    phone_number: str
    is_glav: bool = Field(False)
    role: str = Field(None)
    cabinet_id: Optional[int] = Field(None, gt=0)
    user_id: int = Field(None, gt=0)


@Transaction(propagation=Propagation.REQUIRED_NEW)
async def user_command_create(context: UserDoctorCreateContext) -> UserAndDoctor:
    try:
        query_check_cabinet = (
            select(CabinetDBModel)
            .where(CabinetDBModel.id == context.cabinet_id)
        )
        cursor = await session.execute(query_check_cabinet)
        cab_exists = cursor.scalars().first()
        if cab_exists is None:
            raise NotFoundException(message="Кабинет не найден!")

        hashed_password: str = PasswordHasher.hash_password(context.password)
        query_insert_user = (
            insert(UserDBModel)
            .values(
                login=context.login,
                password=hashed_password
            )
            .returning(UserDBModel)
        )
        cursor = await session.execute(query_insert_user)
        new_user = cursor.scalars().first()

        query_get_role_id = (
            select(RoleDBModel.id)
            .where(RoleDBModel.name == context.role)
        )
        cursor_get_role_id = await session.execute(query_get_role_id)
        role_id = cursor_get_role_id.scalar()
        if role_id is None:
            raise NotFoundException(message="Такая роль не найдена!")

        query_insert_to_user_role = (
            insert(UserRoleDBModel)
            .values(
                user_id=new_user.id,
                role_id=role_id
            )
            .returning(UserRoleDBModel.user_id)
        )
        await session.execute(query_insert_to_user_role)
        doctor_insert_query = (
            insert(DoctorDBModel)
            .values(
                name=context.name,
                last_name=context.last_name,
                patronymic=context.patronymic,
                phone_number=context.phone_number,
                user_id=new_user.id,
                cabinet_id=context.cabinet_id,
                is_glav=context.is_glav,
                author_id=new_user.id if context.user_id is None else context.user_id
            )
        )
        await session.execute(doctor_insert_query)

        query_get_target_user = (
            select(UserDBModel)
            .where(UserDBModel.id == new_user.id)
        )
        cursor = await session.execute(query_get_target_user)
        user_with_details = cursor.scalars().first()
        return UserAndDoctor.model_validate(user_with_details)
    except ValidationError as ve:
        raise ValidationException(message=str(ve))
    except NotFoundException as ne:
        raise ne
    except Exception as e:
        raise InternalServerException(message=str(e))
