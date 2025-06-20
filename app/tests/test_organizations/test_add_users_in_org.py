import pytest
from httpx import AsyncClient, ASGITransport, Cookies

from app.main import app

@pytest.mark.asyncio
async def test_add_users_to_organization(create_organization_and_users, authorized_user):
    organization_id, user_ids = create_organization_and_users

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.post(f"organisation/{organization_id}/add_users/", json=user_ids)
        print(user_ids)
        assert response.status_code == 200
        assert response.json() == {"message": "OK"}

@pytest.mark.asyncio
async def test_add_users_to_nonexistent_organization(create_organization_and_users, authorized_user):
    _, user_ids = create_organization_and_users
    non_existing_org_id = "invalid_org_id"

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        response = await client.post(f"organisation/{non_existing_org_id}/add_users/", json=user_ids)
        assert response.status_code == 404
        assert response.json() == {"detail": "Organization not found"}

@pytest.mark.asyncio
async def test_add_existing_users_to_organization(create_organization_and_users, authorized_user):
    organization_id, user_ids = create_organization_and_users

    client_cookies = Cookies(authorized_user)
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=client_cookies) as client:
        await client.post(f"organisation/{organization_id}/add_users/", json=user_ids)

        response = await client.post(f"organisation/{organization_id}/add_users/", json=user_ids)
        assert response.status_code == 404
        assert response.json() == {"detail": "User already in organization"}