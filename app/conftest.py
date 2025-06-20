import os
import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker

fake = Faker()

os.environ["MODE"]="TEST"

from app.core.bids.schemas import SBidCreate
from app.config import settings
from app.database import async_session_maker, Base, engine
from app.main import app

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session")
async def db_session():
    async with async_session_maker() as session:
        yield session

@pytest.fixture(scope="session")
async def created_user():
    valid_user_data = {
        "username": "testuser12",
        "password": "testuser12"
    }
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        response = await client.post("auth/register/", json=valid_user_data)
        assert response.status_code == 200
    yield valid_user_data


@pytest.fixture(scope="session")
async def authorized_user_empty():
    user_data = {
        "username": "testtesttest12",
        "password": "testtesttest12"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        register_response = await client.post("auth/register/", json=user_data)
        assert register_response.status_code == 200

        user_info = register_response.json()
        user_id = user_info.get("user_id")

        response = await client.post("auth/login/", json={
            "username": user_data["username"],
            "password": user_data["password"]
        })
        assert response.status_code == 200
        assert response.cookies.get("tenders_access_token") is not None

        return {
            "tenders_access_token": response.cookies.get("tenders_access_token"),
            "username": user_data["username"],
            "id": user_id
        }


@pytest.fixture(scope="session")
async def authorized_user():
    user_data = {
        "username": "testtesttest",
        "password": "testtesttest"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        register_response = await client.post("auth/register/", json=user_data)
        assert register_response.status_code == 200

        user_info = register_response.json()
        user_id = user_info.get("user_id")

        response = await client.post("auth/login/", json={
            "username": user_data["username"],
            "password": user_data["password"]
        })
        assert response.status_code == 200
        assert response.cookies.get("tenders_access_token") is not None

        return {
            "tenders_access_token": response.cookies.get("tenders_access_token"),
            "username": user_data["username"],
            "id": user_id
        }


@pytest.fixture(scope="session")
async def created_organization(authorized_user):
    org_request = {
        "name": "Test Organization",
        "description": "Description about test organization",
        "org_type": "LLC"
        }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.post("organisation/new/", json=org_request)
        assert response.status_code == 200

        organization_data = response.json()
        return organization_data

@pytest.fixture(scope="session")
async def create_organization_and_users(authorized_user, created_organization):
    user_ids = []
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        for i in range(24, 27):
            response = await client.post("auth/register/", json={"username": f"testuser{i}", "password": "testpassword"})
            assert response.status_code == 200
            user_id = response.json().get("user_id")
            user_ids.append(user_id)
    return created_organization["organization_id"], user_ids


@pytest.fixture(scope="function")
async def created_tender(created_organization, authorized_user):

    tender_request = {
        "title": fake.sentence(nb_words=5),
        "description": fake.text(max_nb_chars=100),
        "service_type": "CONSTRUCTION"
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.post("tenders/new/", json=tender_request)
        assert response.status_code == 200

        tender_data = response.json()

        return tender_data


@pytest.fixture(scope="function")
async def published_tender(created_tender, authorized_user):
    tender_id = created_tender['id']

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"tenders/{tender_id}/status/", params={"status": "PUBLISHED"})

        assert response.status_code == 200

        updated_tender = response.json()

        return updated_tender

@pytest.fixture(scope="function")
async def created_bid(published_tender, authorized_user):
    bid_data = SBidCreate(
        name=fake.sentence(nb_words=3),
        description=fake.text(max_nb_chars=50)
    )

    tender_id = published_tender["tender"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.post("bids/new/", json=bid_data.model_dump(), params={'tender_id': tender_id, "is_from_organization": True})

        assert response.status_code == 200
        bid = response.json()

        return bid


@pytest.fixture(scope="function")
async def published_bid(created_bid, authorized_user):

    bid_id = created_bid["id"]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/status/", params={"status": "PUBLISHED"})

        assert response.status_code == 200

        published_bid = response.json()

        return published_bid

@pytest.fixture(scope="function")
async def bid_feedback(published_bid, authorized_user):
    bid_id = published_bid['id']

    feedback_data = {
        "feedback": "Good feedback"
    }
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test", cookies=authorized_user) as client:
        response = await client.put(f"bids/{bid_id}/feedback/", json=feedback_data)





