from shared.db.db_session import session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from shared.db.models.user import UserDBModel
from core.hsn.doctor.schemas import UserAndDoctor
from loguru import logger


async def hsn_user_get_me(user_id: int):
    query = (
        select(UserDBModel)
        .where(UserDBModel.id == user_id)
    )
    cursor = await session.execute(query)

    user = cursor.unique().scalars().first()
    model = UserAndDoctor(
        id=user.id,
        login=user.login,
        roles=user.roles,
        doctor=user.doctor
    )
    return model
