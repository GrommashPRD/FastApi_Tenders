import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_all_tenders(authorized_user):

    tender_request = {
        "title": "Test Tender v2",
        "description": "This is a description for the test tender v2",
        "service_type": "CONSTRUCTION"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response_new = await client.post("tenders/new/", json=tender_request)
        assert response_new.status_code == 200
        response_new_json = response_new.json()
        tender_id = response_new_json["id"]
        response_pub = await client.put(f"tenders/{tender_id}/status/", params={"status": "PUBLISHED"})
        assert response_pub.status_code == 200
        response_all = await client.get("tenders/")
        assert response_all.status_code == 200
        response_all_json = response_all.json()
        assert isinstance(response_all_json["tenders"], list)
        assert len(response_all_json) != 0