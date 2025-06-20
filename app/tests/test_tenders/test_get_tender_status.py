import os

os.environ["MODE"]="TEST"

import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_get_tender_no_permission(created_tender, authorized_user_empty, authorized_user):
    tender_id = created_tender['id']

    client_auth_cookies = Cookies(authorized_user)
    client_not_auth_cookies = Cookies(authorized_user_empty)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_auth_cookies) as client:
        await client.put(f"tenders/{tender_id}/status/", params={"status": "CREATED"})
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test",
                               cookies=client_not_auth_cookies) as client:
        response = await client.get(f"tenders/{tender_id}/status/")

        assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_tender_status(created_tender, authorized_user):
    tender_id = created_tender['id']

    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.get(f"tenders/{tender_id}/status/")
        assert response.status_code == 200

        tender_data = response.json()
        expected_status_created = "CREATED"
        expected_status_published = "PUBLISHED"
        expected_status_updated = "CLOSE"
        assert tender_data['status'] == expected_status_created or expected_status_published or expected_status_updated





