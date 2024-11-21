from loguru import logger
from sqlalchemy import insert, select
from shared.db.models.role import RoleDBModel
from shared.db.db_session import db_session, SessionContext


@SessionContext()
async def hsn_create_role_doctor():
    query_check_role_exists = select(RoleDBModel).where(RoleDBModel.name == "doctor")
    cursor = await db_session.execute(query_check_role_exists)
    role_exists = cursor.scalars().first()
    if role_exists:
        return

    query = insert(RoleDBModel).values(name="doctor")
    cursor = await db_session.execute(query)
    await db_session.commit()
    logger.debug("Role doctor setup complete!")
