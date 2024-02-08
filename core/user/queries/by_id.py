from sqlalchemy import select

from shared.db.db_session import SessionContext, db_session
from typing import Optional
from core.user.model import User
from shared.db.models import UserDBModel


@SessionContext()
async def user_query_by_id(user_id: int) -> Optional[User]:
    query = select(UserDBModel).where(UserDBModel.id == user_id, UserDBModel.is_active == True)
    cursor = await db_session.execute(query)

    result = cursor.first()
    if result is None:
        return None

    return User.model_validate(result[UserDBModel])