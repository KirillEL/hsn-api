import random

from httpx import AsyncClient


async def test_login(ac: AsyncClient, test_user):
    response = await ac.post("/auth/login", json=test_user)
    print(response.text)
    assert response.status_code == 200
    token = response.json()["token"]
    assert token is not None
    return token


async def test_create_med_org(ac: AsyncClient, test_user):
    token = await test_login(ac, test_user)
    unique_num = 1 + random.randint(1, 5000)
    payload = {
        "name": "fff",
        "number": unique_num,
        "address": "address"
    }
    response = await ac.post("/admin/med_organizations", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response_data = response.json()
    id = response_data.get('id')
    return id


async def test_get_list_med_orgs(ac: AsyncClient, test_user):
    token = await test_login(ac, test_user)
    response = await ac.get("/admin/med_organizations", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
