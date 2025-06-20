import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_create_organization_success(authorized_user):
    org_request = {
            "name": "testorganization",
            "description": "description about testorganization",
            "org_type": "LLC"
        }

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        # Создаем организацию, передавая куки
        response = await client.post("organisation/new/", json=org_request)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["message"] == "Organization created successfully"
        assert response_json["organization_name"] == org_request["name"]

@pytest.mark.asyncio
async def test_create_existing_organization(authorized_user):
    org_request = {
        "name": "testorganization",
        "description": "description about testorganization",
        "org_type": "LLC"
    }

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        # Создаем организацию, передавая куки
        response = await client.post("organisation/new/", json=org_request)

        assert response.status_code == 400
        response_json = response.json()
        assert response_json["detail"] == "Organization already exists"

@pytest.mark.asyncio
async def test_create_invalid_organization_data(authorized_user):
    org_request = {
            "name": "",
            "description": "description about testorganization",
            "org_type": "LLC"
    }

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        # Создаем организацию, передавая куки
        response = await client.post("organisation/new/", json=org_request)

        assert response.status_code == 400
        response_json = response.json()
        assert response_json["detail"] == "Organization name is required"

