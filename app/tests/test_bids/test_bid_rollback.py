import pytest
from httpx import AsyncClient, ASGITransport

from app.core.bids.schemas import SBidUpdate

from app.main import app




@pytest.mark.asyncio
async def test_rollback_tender(created_bid, authorized_user):
    bid_id = created_bid['id']
    update_data = SBidUpdate(name="New v2", description="Test description v2")

    version = 1

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.patch(f"bids/{bid_id}/edit", json=update_data.model_dump())
        assert response.status_code == 200

        response = await client.put(f"bids/{bid_id}/rollback/{version}", params={"version": version})
        assert response.status_code == 200
        response_json = response.json()

        assert response_json["version"] == 2

@pytest.mark.asyncio
async def test_rollback_tender(created_bid, authorized_user):
    bid_id = '40c40041-c88b-4331-8ce0-8199e5c80939'

    version = 1

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:

        response = await client.put(f"bids/{bid_id}/rollback/{version}", params={"version": version})
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Bid not found."


@pytest.mark.asyncio
async def test_rollback_tender(created_bid, authorized_user):
    bid_id = created_bid['id']
    update_data = SBidUpdate(name="New v2", description="Test description v2")

    version = 99

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.patch(f"bids/{bid_id}/edit", json=update_data.model_dump())
        assert response.status_code == 200

        response = await client.put(f"bids/{bid_id}/rollback/{version}", params={"version": version})
        assert response.status_code == 404
        response_json = response.json()

        assert response_json["detail"] == "Version not found"

