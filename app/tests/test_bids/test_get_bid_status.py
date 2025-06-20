import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_get_update_bid_status(created_bid, authorized_user):
    bid_id = created_bid["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.get(f"bids/{bid_id}/status/")

        assert response.status_code == 200
        response_json = response.json()
        assert "Status" in response_json

@pytest.mark.asyncio
async def test_get_update_bid_status_failed(created_bid, authorized_user_empty):

    bid_id = created_bid["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.get(f"bids/{bid_id}/status/")

        assert response.status_code == 403
        response_json = response.json()
        assert response_json["detail"] == "You dont have permissions"
