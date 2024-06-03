import pytest
from httpx import AsyncClient
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.models import CabinetDBModel
from shared.db.models.role import RoleDBModel


async def test_register(ac: AsyncClient, session: AsyncSession):

    query = (
        select(CabinetDBModel)
    )
    cursor = await session.execute(query)
    cabinet = cursor.scalars().all()
    print(cabinet)
    assert len(cabinet) > 0

    test_payload = {
        "login": "k12345",
        "password": "k12345",
        "name": "log3",
        "last_name": "k123",
        "patronymic": "k123",
        "phone_number": "+79137689477",
        "is_glav": False,
        "role": "doctor",
        "cabinet_id": 1
    }
    response = await ac.post("/auth/register", json=test_payload)
    print(response.text)
    assert response.status_code == 200
    assert response.json()["id"] is not None
