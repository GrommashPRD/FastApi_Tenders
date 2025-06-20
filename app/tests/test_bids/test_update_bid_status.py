import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_update_bid_status(created_bid, authorized_user):
    bid_id = created_bid["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/status/", params={"status": "PUBLISHED"})

        assert response.status_code == 200

        response_json = response.json()
        assert "Bid id" in response_json
        assert response_json["Bid id"] == bid_id
        assert "New status" in response_json


@pytest.mark.asyncio
async def test_update_bid_status(created_bid, authorized_user_empty):
    bid_id = created_bid["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.put(f"bids/{bid_id}/status/", params={"status": "PUBLISHED"})

        assert response.status_code == 403

        response_json = response.json()
        assert response_json["detail"] == "User dont have permissions"