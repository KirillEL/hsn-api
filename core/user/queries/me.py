from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from shared.db.models.user import UserDBModel
from core.hsn.doctor.model import UserAndDoctor


@SessionContext()
async def hsn_user_get_me(user_id: int):
    query = (
        select(UserDBModel)
        .options(joinedload(UserDBModel.doctor))
        .where(UserDBModel.id == user_id)
    )
    cursor = await db_session.execute(query)

    user = cursor.unique().scalars().first()

    model = UserAndDoctor(
        id=user.id,
        login=user.login,
        role=user.role,
        doctor=user.doctor
    )
    return model