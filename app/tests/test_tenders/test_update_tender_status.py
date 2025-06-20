import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_get_tender_status(created_tender, authorized_user):
    tender_id = created_tender['id']

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.put(f"tenders/{tender_id}/status/", params={"status": "PUBLISHED"})
        assert response.status_code == 200

        tender_data = response.json()

        expected_status_published = "PUBLISHED"
        assert tender_data['new status'] == expected_status_published


@pytest.mark.asyncio
async def test_get_unpublished_tender_status(created_tender, authorized_user_empty):
    tender_id = created_tender['id']

    client_cookies = Cookies(authorized_user_empty)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies, params={"status": "PUBLISHED"}) as client:
        response = await client.put(f"tenders/{tender_id}/status/")
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Organization responsible not found"


