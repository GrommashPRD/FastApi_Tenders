import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_rollback_tender(created_tender, authorized_user):
    tender_id = created_tender['id']

    new_description = {
        "description": "New description about tender z",
    }

    version = 1

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        # Тут у нас уже v2
        response = await client.patch(f"tenders/{tender_id}/edit", json=new_description)
        assert response.status_code == 200

        response = await client.put(f"tenders/{tender_id}/rollback/{version}", params={"version":version})

        assert response.status_code == 200
        response_json = response.json()

        assert response_json["new version"] == 3
        assert response_json["new description"] == created_tender["description"]


@pytest.mark.asyncio
async def test_rollback_tender_failed(created_tender, authorized_user):
    tender_id = created_tender['id']

    new_description = {
        "description": "New description about tender z",
    }

    version = 99

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.patch(f"tenders/{tender_id}/edit", json=new_description)
        assert response.status_code == 200

        response = await client.put(f"tenders/{tender_id}/rollback/{version}", params={"version":version})

        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Version 99 not found"

@pytest.mark.asyncio
async def test_rollback_tender_to_zero_version(created_tender, authorized_user):
    tender_id = created_tender['id']

    new_description = {
        "description": "New description about tender z",
    }

    version = 0

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.patch(f"tenders/{tender_id}/edit", json=new_description)
        assert response.status_code == 200

        response = await client.put(f"tenders/{tender_id}/rollback/{version}", params={"version":version})

        assert response.status_code == 422
        response_json = response.json()
        assert response_json["detail"] == "version must be an integer and greater than 0"
