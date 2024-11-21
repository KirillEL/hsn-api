from httpx import AsyncClient


async def test_get_list_patients(ac: AsyncClient, test_token):
    response = await ac.get(
        "/patients", headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200


async def test_create_patient(ac: AsyncClient, test_token):
    test_payload = {
        "name": "string333",
        "last_name": "string333",
        "gender": "М",
        "birth_date": "07.04.2001",
        "location": "Новосибирск",
        "district": "stringQQQQ",
        "address": "stringQQQQ",
        "phone": "+79137689042",
        "clinic": "string",
        "disability": "нет",
        "lgota_drugs": "нет",
        "has_hospitalization": False,
        "count_hospitalization": 0,
    }
    response = await ac.post(
        "/patients",
        json=test_payload,
        headers={"Authorization": f"Bearer {test_token}"},
    )
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["id"] is not None
    return response_data["id"]


async def test_get_patient_by_id(ac: AsyncClient, test_token):
    created_patient_id = await test_create_patient(ac, test_token)
    response = await ac.get(
        f"/patients/{created_patient_id}",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] is not None
