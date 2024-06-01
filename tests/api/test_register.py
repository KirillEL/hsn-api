import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models.role import RoleDBModel


async def test_register(session: AsyncSession):
    session = session

    query = (
        select(RoleDBModel)
        .where(RoleDBModel.name == "admin")
    )
    cursor = await session.execute(query)
    role = cursor.scalars().first()
    assert role is not None
