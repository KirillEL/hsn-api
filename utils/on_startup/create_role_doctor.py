from loguru import logger
from sqlalchemy import insert, select

from shared.db import Transaction
from shared.db.models.role import RoleDBModel
from shared.db.db_session import session
from shared.db.transaction import Propagation


@Transaction(propagation=Propagation.REQUIRED)
async def hsn_create_role_doctor():
    query_check_role_exists = (
        select(RoleDBModel)
        .where(RoleDBModel.name == "doctor")
    )
    cursor = await session.execute(query_check_role_exists)
    role_exists = cursor.scalars().first()
    if role_exists:
        return

    query = (
        insert(RoleDBModel)
        .values(
            name="doctor"
        )
    )
    await session.execute(query)
    logger.debug('Role doctor setup complete!')