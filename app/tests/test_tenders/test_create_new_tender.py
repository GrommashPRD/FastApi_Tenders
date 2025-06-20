import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_create_new_tender_success(authorized_user):
    tender_data = {
        "title": "New Tender",
        "description": "Description about New Tender",
        "service_type": "CONSTRUCTION",
    }

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.post("tenders/new/", json=tender_data)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == tender_data["title"]
        assert response_json["description"] == tender_data["description"]


@pytest.mark.asyncio
async def test_create_existing_tender(authorized_user):
    tender_data = {
        "title": "New Tender",
        "description": "Description about New Tender",
        "service_type": "CONSTRUCTION",
    }

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.post("tenders/new/", json=tender_data)

        assert response.status_code == 400
        response_json = response.json()
        assert response_json["detail"] == "Tender already exists."


@pytest.mark.asyncio
async def test_create_new_tender_without_auth():
    tender_data = {
        "title": "New Tender",
        "description": "Description about New Tender",
        "service_type": "CONSTRUCTION",
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=None) as client:
        response = await client.post("tenders/new/", json=tender_data)

        assert response.status_code == 401
        response_json = response.json()
        assert response_json["detail"] == "Invalid token"

