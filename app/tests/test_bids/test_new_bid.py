import pytest
from httpx import AsyncClient, ASGITransport

from app.core.bids.schemas import SBidCreate
from app.main import app

@pytest.mark.asyncio
async def test_create_bid_for_non_published_tender(created_tender, authorized_user):
    bid_data = SBidCreate(name="Test Bid", description="This is a test bid description")
    tender_id = created_tender["id"]  # Получаем тендер с не опубликованным статусом

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.post(
            "bids/new/",
            json=bid_data.model_dump(),
            params={
                "tender_id": tender_id,
                "is_from_organization": True
            }
        )

        assert response.status_code == 404
        assert response.json().get("detail") == "Tender is non-published"

@pytest.mark.asyncio
async def test_create_bid_for_published_tender(created_tender, authorized_user):
    bid_data = SBidCreate(name="Test Bid", description="This is a test bid description")
    tender_id = created_tender["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        await client.put(f"/tenders/{tender_id}/status/", params={"status": "PUBLISHED"})

        response = await client.post(
            "bids/new/",
            json=bid_data.model_dump(),
            params={
                "tender_id": tender_id,
                "is_from_organization": True
            }
        )

        assert response.status_code == 200

        new_bid = response.json()
        assert new_bid.get("id") is not None
