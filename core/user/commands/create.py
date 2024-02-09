
from shared.db.db_session import SessionContext, db_session
from pydantic import BaseModel, Field
from core.user import UserFlat
from sqlalchemy import insert, select
from shared.db.models.user import UserDBModel
from utils import HashHelper


class UserCreateContext(BaseModel):
    user_id: int = Field(None, gt=0)
    login: str = Field(None, max_length=25)
    password: str = Field(None, min_length=6)


@SessionContext()
async def user_command_create(context: UserCreateContext) -> UserFlat:
    payload = context.model_dump(exclude={'user_id'})
    payload['password'] = HashHelper.hash_password(payload['password'])
    payload['author_id'] = context.user_id
    model = UserDBModel(**payload)
    db_session.add(model)
    await db_session.commit()
    await db_session.refresh(model)
    return model


