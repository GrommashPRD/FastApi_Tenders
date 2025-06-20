import pytest
from httpx import AsyncClient, ASGITransport


from app.main import app

@pytest.mark.asyncio
async def test_bid_feedback_success(published_bid, authorized_user):

    bid_id = published_bid['id']

    feedback_data = {
        "feedback": "Good feedback"
    }
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/feedback/", json=feedback_data)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["message"] == "OK"

@pytest.mark.asyncio
async def test_no_bid_feedback(created_bid, authorized_user):

    bid_id = "4d861e52-74ca-437d-a7ca-aed2587a18d6"

    feedback_data = {
        "feedback": "Good feedback"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/feedback/", json=feedback_data)

        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Bid not found"

@pytest.mark.asyncio
async def test_no_bid_feedback_permissions(created_bid, authorized_user_empty):

    bid_id = created_bid['id']

    feedback_data = {
        "feedback": "Good feedback"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.put(f"bids/{bid_id}/feedback/", json=feedback_data)

        assert response.status_code == 403
        response_json = response.json()
        assert response_json["detail"] == "You don't have the rights for this action"

