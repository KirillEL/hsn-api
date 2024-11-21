from shared.db.db_session import SessionContext, db_session
from infra.config import config
from shared.db.models.role import RoleDBModel
from shared.db.models.user import UserDBModel
from shared.db.models.user_role import UserRoleDBModel
from sqlalchemy import select, func, insert
from utils.password_helper import PasswordHasher
from loguru import logger


@SessionContext()
async def hsn_create_admin():
    query_check_admin_role = (
        select(func.count()).select_from(RoleDBModel).where(RoleDBModel.name == "admin")
    )
    result = await db_session.execute(query_check_admin_role)
    admin_count = result.scalar()
    if admin_count == 0:
        role = RoleDBModel(name="admin")
        db_session.add(role)
        await db_session.commit()

        admin_role_id = role.id
    else:
        role = await db_session.execute(
            select(RoleDBModel).where(RoleDBModel.name == "admin")
        )
        admin_role_id = role.scalar_one().id

    query_check_admin_user = (
        select(func.count())
        .select_from(UserDBModel)
        .join(UserRoleDBModel)
        .where(UserRoleDBModel.role_id == admin_role_id)
    )
    res = await db_session.execute(query_check_admin_user)
    admin_user_count = res.scalar()

    if admin_user_count == 0:
        new_user = UserDBModel(
            login="admin%&", password=PasswordHasher.hash_password(config.ADMIN_PASS)
        )
        db_session.add(new_user)
        await db_session.flush()

        query_add_user_role = (
            insert(UserRoleDBModel)
            .values(user_id=new_user.id, role_id=admin_role_id)
            .returning(UserRoleDBModel.user_id)
        )
        await db_session.execute(query_add_user_role)
        await db_session.commit()

        logger.debug("Admin setup complete...")
