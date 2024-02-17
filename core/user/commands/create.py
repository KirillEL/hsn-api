from typing import Optional

from shared.db.db_session import SessionContext, db_session
from pydantic import BaseModel, Field
from core.hsn.doctor.model import UserAndDoctor
from sqlalchemy import insert, select
from shared.db.models.user import UserDBModel
from shared.db.models.doctor import DoctorDBModel
from utils import cipher

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


@SessionContext()
async def user_command_create(context: UserDoctorCreateContext) -> UserAndDoctor:
    doctor_payload = context.model_dump(exclude={'login', 'password', 'user_id'})
    query = (
        insert(UserDBModel)
        .values(
            login=context.login,
            password=cipher.encrypt(context.password)
        )
        .returning(UserDBModel)
    )
    cursor = await db_session.execute(query)
    new_user = cursor.first()[0]

    query_doctor = (
        insert(DoctorDBModel)
        .values(
            user_id=new_user.id,
            author_id=new_user.id,
            **doctor_payload
        )
        .returning(DoctorDBModel)
    )
    cursor_2 = await db_session.execute(query_doctor)
    new_doctor = cursor_2.first()[0]

    model = UserAndDoctor(
        id=new_user.id,
        login=new_user.login,
        role=new_user.role,
        doctor=new_doctor
    )

    await db_session.commit()

    return UserAndDoctor.model_validate(model)
