from sqlalchemy import select
from sqlalchemy.orm import joinedload
from shared.db.db_session import SessionContext, db_session
from typing import Optional
from core.user.model import UserFlat, User
from shared.db.models import UserDBModel


@SessionContext()
async def user_query_by_id(user_id: int) -> Optional[UserFlat]:
    query = (
        select(UserDBModel)
        .options(joinedload(UserDBModel.roles))
        .where(UserDBModel.id == user_id, UserDBModel.is_active.is_(True))
    )

    cursor = await db_session.execute(query)

    result = cursor.scalars().first()

    if result is None:
        return None

    return UserFlat.model_validate(result)
