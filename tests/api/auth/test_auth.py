import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from shared.db.models import UserDBModel, CabinetDBModel, MedOrganizationDBModel
from shared.db.models.role import RoleDBModel
from tests.conftest import test_async_session_factory, set_up_cabinet


@pytest.mark.asyncio
async def test_create_cabinet(cabinet_id):
    assert cabinet_id is not None


@pytest.mark.asyncio
async def test_exist_roles(transaction):
    doctor_role = await transaction.execute(select(RoleDBModel).where(RoleDBModel.name == 'doctor'))
    admin_role = await transaction.execute(select(RoleDBModel).where(RoleDBModel.name == 'admin'))
    assert doctor_role.scalar_one() is not None
    assert admin_role.scalar_one() is not None


@pytest.mark.asyncio
async def test_exist_admin_user(transaction):
    query = (
        select(UserDBModel)
        .where(UserDBModel.login == "admin%&")
    )
    cursor = await transaction.execute(query)
    admin = cursor.scalar_one()
    assert admin is not None


@pytest.mark.asyncio
async def test_register(ac: AsyncClient, test_user, cabinet_id):
    payload = {
        "login": test_user.get("login"),
        "password": test_user.get("password"),
        "name": "qwerty",
        "last_name": "fafea",
        "phone_number": "+76230000000",
        "is_glav": True,
        "role": "doctor",
        "cabinet_id": cabinet_id,
        "author_id": 1
    }
    response = await ac.post("/auth/register", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login(ac: AsyncClient, test_user):
    response = await ac.post("/auth/login", json=test_user)
    print(response.text)
    assert response.status_code == 200
    token = response.json()["token"]
    assert token is not None
    return token


@pytest.mark.asyncio
async def test_verify(ac: AsyncClient, test_user):
    token = await test_login(ac=ac, test_user=test_user)
    assert token is not None
    response = await ac.post("/auth/verify", json={"token": token})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_me(ac: AsyncClient, test_user):
    token = await test_login(ac=ac, test_user=test_user)
    response = await ac.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
