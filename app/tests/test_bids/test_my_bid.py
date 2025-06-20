import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_get_my_bid(created_bid, authorized_user):

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.get("bids/my/")

        assert response.status_code == 200
        response_json = response.json()
        assert "bids" in response_json
        assert response_json["bids"]

@pytest.mark.asyncio
async def test_get_my_bid_failed(authorized_user_empty):

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.get("bids/my/")

        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "No bids found"