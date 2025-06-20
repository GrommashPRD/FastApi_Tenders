import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_put_decision_accept(published_bid, authorized_user):
    bid_id = published_bid['id']

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/submit_decision", params={"status":"ACCEPTED"})
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['message'] == "OK"

@pytest.mark.asyncio
async def test_put_decision_not_published(created_bid, authorized_user):
    bid_id = created_bid['id']

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/submit_decision", params={"status":"ACCEPTED"})
        assert response.status_code == 400
        response_json = response.json()
        assert response_json["detail"] == 'Non-published bid'

@pytest.mark.asyncio
async def test_put_decision_rejected(published_bid, authorized_user):
    bid_id = published_bid['id']

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/submit_decision", params={"status":"REJECTED"})
        assert response.status_code == 200
