import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_get_my_tenders(authorized_user):
    client_cookies = Cookies(authorized_user)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.get("tenders/my/")

        assert response.status_code == 200
        response_json = response.json()
        assert isinstance(response_json["tenders"], list)
        assert len(response_json) != 0