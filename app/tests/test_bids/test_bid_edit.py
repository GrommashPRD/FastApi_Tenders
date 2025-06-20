import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_bid_edit(created_bid, authorized_user):
    bid_id = created_bid["id"]

    print(f"Initial Bid Status: {created_bid['status']}")

    update_data = {
        "name": "string",
        "description": "string"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.patch(f"bids/{bid_id}/edit", json=update_data)

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_bid_id_not_found(created_bid, authorized_user):
    bid_id = "4d861e52-84ca-437d-a7ca-aed2587a18d6"

    update_data = {
        "name": "string",
        "description": "string"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.patch(f"bids/{bid_id}/edit", json=update_data)

        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Bid not found."

@pytest.mark.asyncio
async def test_update_bid_id_not_found(created_bid, authorized_user_empty):
    bid_id = created_bid["id"]

    update_data = {
        "name": "string",
        "description": "string"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.patch(f"bids/{bid_id}/edit", json=update_data)

        assert response.status_code == 403
        response_json = response.json()
        assert response_json["detail"] == "You don't have the rights for this action"