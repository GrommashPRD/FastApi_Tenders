import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_update_tender(created_tender, authorized_user):
    tender_id = created_tender['id']

    new_tender_data = {
        "description": "New description about tender z",
    }

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.patch(f"tenders/{tender_id}/edit", json=new_tender_data)
        assert response.status_code == 200
        response_json = response.json()

        assert response_json["message"] == "OK"

@pytest.mark.asyncio
async def test_update_tender_failed(created_tender, authorized_user):
    tender_id = created_tender['id']

    new_tender_data = {
        "description": "",
    }

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.patch(f"tenders/{tender_id}/edit", json=new_tender_data)
        assert response.status_code == 400
        response_json = response.json()

        assert response_json["detail"] == "Description cannot be empty"

@pytest.mark.asyncio
async def test_update_tender_with_no_description(created_tender, authorized_user):
    tender_id = created_tender['id']

    new_tender_data = {
        "description": "",
    }

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.patch(f"tenders/{tender_id}/edit", json=new_tender_data)

        assert response.status_code == 400
        response_json = response.json()

        assert response_json["detail"] == "Description cannot be empty"


@pytest.mark.asyncio
async def test_update_tender_with_no_permissions(created_tender, authorized_user_empty):
    tender_id = created_tender['id']

    new_tender_data = {
        "description": "",
    }

    client_cookies = Cookies(authorized_user_empty)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.patch(f"tenders/{tender_id}/edit", json=new_tender_data)

        assert response.status_code == 404
        response_json = response.json()

        assert response_json["detail"] == "Organization responsible not found"

