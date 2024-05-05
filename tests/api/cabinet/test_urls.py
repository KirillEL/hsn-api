from httpx import AsyncClient

from api.routes.admin.cabinets import CreateCabinetDto
from tests.api.med_org.test_urls import test_create_med_org


async def test_login(ac: AsyncClient, test_user):
    response = await ac.post("/auth/login", json=test_user)
    print(response.text)
    assert response.status_code == 200
    token = response.json()["token"]
    assert token is not None
    return token


async def test_create_cabinet(ac: AsyncClient, test_user):
    token = await test_login(ac, test_user)
    med_org_id = await test_create_med_org(ac, test_user)
    model = {
        "number":"f123",
        "med_id": med_org_id
    }
    response = await ac.post("/admin/cabinets", json=model, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response_data = response.json()
    id = response_data.get('id')
    return id
