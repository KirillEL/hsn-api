from shared.db.db_session import db_session, SessionContext
from sqlalchemy import select
from shared.db.models.user import UserDBModel
from shared.db.models.doctor import DoctorDBModel
from core.hsn.doctor.model import UserAndDoctor


@SessionContext()
async def hsn_user_get_me(user_id: int):
    query = (
        select(UserDBModel, DoctorDBModel)
        .where(UserDBModel.id == user_id)
    )
    cursor = await db_session.execute(query)
    user = cursor.all()[0]
  
    model = UserAndDoctor(
        id=user[0].id,
        login=user[0].login,
        role=user[0].role,
        doctor=user[1]
    )
    return model
