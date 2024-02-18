import hashlib
from typing import Optional

from sqlalchemy import select, func
from shared.db.db_session import SessionContext, db_session
from ..model import User
from shared.db.models.user import UserDBModel
from utils import PasswordHasher


@SessionContext()
async def user_query_login(username: str, password: str) -> Optional[User]:
    query = (
        select(UserDBModel)
        .where(func.lower(UserDBModel.login) == func.lower(username))
    )

    cursor = await db_session.execute(query)
    user_db = cursor.scalars().first()
    if user_db is None:
        return None

    if PasswordHasher.verify_password(hashed_password=user_db.password, plain_password=password):
        return User.from_orm(user_db)
    else:
        return None
