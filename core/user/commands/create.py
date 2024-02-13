from shared.db.db_session import SessionContext, db_session
from pydantic import BaseModel, Field
from core.user import UserFlat
from sqlalchemy import insert, select
from shared.db.models.user import UserDBModel
from utils import HashHelper


class UserCreateContext(BaseModel):
    login: str = Field(None, max_length=25)
    password: str = Field(None, min_length=6)


@SessionContext()
async def user_command_create(context: UserCreateContext) -> UserFlat:
    payload = context
    payload.password = HashHelper.hash_password(context.password)
    model = UserDBModel(**payload.dict())
    db_session.add(model)
    await db_session.commit()
    await db_session.refresh(model)
    return model
