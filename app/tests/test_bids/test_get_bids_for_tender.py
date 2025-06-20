import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_get_all_bids_for_tender(published_tender, authorized_user):
    tender_id = published_tender["tender"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.get(f"bids/{tender_id}/list/")

        assert response.status_code == 200
        response_json = response.json()
        assert isinstance(response_json, dict)
        assert len(response_json) != 0


@pytest.mark.asyncio
async def test_get_all_bids_failed(created_tender, authorized_user_empty):
    tender_id = created_tender["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.get(f"bids/{tender_id}/list/")

        print(tender_id)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Organization responsible not found"

@pytest.mark.asyncio
async def test_get_all_bids_invalid_tender_id(created_tender, authorized_user_empty):
    tender_id = '33c562e5-842f-47c4-b59d-27790508bb43'

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:
        response = await client.get(f"bids/{tender_id}/list/")

        print(tender_id)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Tender not found"

@pytest.mark.asyncio
async def test_get_all_bids_(created_tender, authorized_user, authorized_user_empty):
    tender_id = created_tender["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        await client.put(f"/tenders/{tender_id}/status/", params={"status": "PUBLISHED"})

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user_empty) as client:

        response = await client.get(f"bids/{tender_id}/list/")

        print(tender_id)
        assert response.status_code == 404
        response_json = response.json()
        assert response_json["detail"] == "Organization responsible not found"
