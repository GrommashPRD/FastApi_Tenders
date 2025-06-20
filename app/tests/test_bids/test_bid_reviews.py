import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_get_bids_feedback(created_tender, authorized_user):
    tender_id = created_tender["id"]
    username = authorized_user["username"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.get(f"bids/{tender_id}/reviews", params={"author_username": username})

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_bids_feedback(created_tender, authorized_user):
    tender_id = "0ce8840d-d348-4f2e-bb82-cf344d138834"
    username = authorized_user["username"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.get(f"bids/{tender_id}/reviews", params={"author_username": username})

        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Tender not found."

@pytest.mark.asyncio
async def test_get_bids_feedback(created_tender, authorized_user_empty, authorized_user):
    tender_id = created_tender["id"]
    username = authorized_user_empty["username"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.get(f"bids/{tender_id}/reviews", params={"author_username": username})

        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "User organization not found"