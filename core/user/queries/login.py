import hashlib
from typing import Optional

from sqlalchemy import select, func
from shared.db.db_session import SessionContext, db_session
from ..model import User
from shared.db.models.user import UserDBModel
from utils import cipher


@SessionContext()
async def user_query_login(username: str, password: str) -> Optional[User]:
    query = select(UserDBModel)
    query = query.where(func.lower(UserDBModel.login) == func.lower(username))

    cursor = await db_session.execute(query)
    res = cursor.first()
    if res is None:
        return None

    user_db = res[0]

    hashed_password = cipher.encrypt(password)

    return None if user_db.password != hashed_password else User.model_validate(user_db)
