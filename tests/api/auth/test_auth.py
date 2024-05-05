import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from shared.db.models import UserDBModel
from shared.db.models.role import RoleDBModel
from tests.conftest import test_async_session_factory


async def test_exist_roles():
    async with test_async_session_factory.begin() as session:
        doctor_role = await session.execute(select(RoleDBModel).where(RoleDBModel.name == 'doctor'))
        admin_role = await session.execute(select(RoleDBModel).where(RoleDBModel.name == 'admin'))
        assert doctor_role.scalar_one() is not None
        assert admin_role.scalar_one() is not None


async def test_exist_admin_user(test_user):
    async with test_async_session_factory.begin() as session:
        query = (
            select(UserDBModel)
            .where(UserDBModel.login == test_user.get('login'))
        )
        cursor = await session.execute(query)
        admin = cursor.scalar_one()
        print(admin.__dict__)
        assert admin is not None


async def test_login(ac: AsyncClient, test_user):
    response = await ac.post("/auth/login", json=test_user)
    print(response.text)
    assert response.status_code == 200
    token = response.json()["token"]
    assert token is not None
    return token


async def test_register(ac: AsyncClient):
    payload = {
        "login": "v1111",
        "password": "<PASSWORD>",
        "name": "fvad",
        "last_name": "fafea",
        "phone_number": "+79135433212",
        "is_glav": False,
        "role": "doctor",
        "cabinet_id": 1
    }
    response = await ac.post("/auth/register", json=payload)
    assert response.status_code == 200


async def test_verify(ac: AsyncClient, test_user: dict):
    token = await test_login(ac, test_user)
    assert token is not None
    response = await ac.post("/auth/verify", json={"token": token})
    assert response.status_code == 200


async def test_user_me(ac: AsyncClient, test_user: dict):
    token = await test_login(ac, test_user)
    response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
