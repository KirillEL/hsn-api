from typing import Optional

from shared.db.db_session import SessionContext, db_session
from pydantic import BaseModel, Field
from core.hsn.doctor.model import UserAndDoctor
from sqlalchemy import insert, select
from shared.db.models.user import UserDBModel
from shared.db.models.doctor import DoctorDBModel
from utils import PasswordHasher
from api.exceptions import BadRequestException


class UserDoctorCreateContext(BaseModel):
    login: str = Field(None, max_length=25)
    password: str = Field(None, min_length=6)
    name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    patronymic: Optional[str] = Field(..., max_length=100)
    phone_number: int = Field(..., gt=0)
    is_glav: bool = Field(False)
    cabinet_id: Optional[int] = Field(None, gt=0)
    user_id: int = Field(None, gt=0)


async def create_user(context: UserDoctorCreateContext):
    hashed_password = PasswordHasher.hash_password(context.password)
    query = (
        insert(UserDBModel)
        .values(
            login=context.login,
            password=hashed_password
        )
        .returning(UserDBModel)
    )
    result = await db_session.execute(query)
    await db_session.commit()
    return result.scalars().first()


async def create_doctor(context: UserDoctorCreateContext, user_id: int):
    doctor_payload = context.model_dump(exclude={'login', 'password', 'user_id'})
    query = (
        insert(DoctorDBModel)
        .values(
            **doctor_payload,
            user_id=user_id,
            author_id=user_id
        )
        .returning(DoctorDBModel)
    )
    result = await db_session.execute(query)
    await db_session.commit()
    return result.scalars().first()


@SessionContext()
async def user_command_create(context: UserDoctorCreateContext) -> UserAndDoctor:
    try:
        new_user = await create_user(context)
        new_doctor = await create_doctor(context, new_user.id)
        return UserAndDoctor.model_validate(
            dict(id=new_user.id, login=new_user.login, role=new_user.role, doctor=new_doctor))
    except Exception as e:
        await db_session.rollback()
        raise BadRequestException(message=str(e))
