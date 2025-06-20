import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

class TestRegisterUser:
    """Тесты для эндпоинта регистрации пользователя"""

    @pytest.fixture
    def valid_user_data(self):
        """Валидные данные пользователя для тестов"""
        return {
            "username": "testuser122",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }

    @pytest.fixture
    def invalid_user_data(self):
        """Невалидные данные пользователя для тестов"""
        return {
            "username": "",
            "password": "123",
            "first_name": "",
            "last_name": ""
        }

    @pytest.fixture
    def unicode_user_data(self):
        """Невалидные данные пользователя для тестов"""
        return {
            "username": "тестовыйюзер",
            "password": "пароль123",
            "first_name": "Тест",
            "last_name": "Юзер"
        }

    @pytest.mark.asyncio
    async def test_register_success(self, valid_user_data):
        async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
            response = await client.post("auth/register/", json=valid_user_data)

            assert response.status_code == 200
            response_json = response.json()
            assert response_json["message"] == "OK"

    @pytest.mark.asyncio
    async def test_register_failure(self, invalid_user_data):
        async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
            response = await client.post("auth/register/", json=invalid_user_data)

            assert response.status_code == 400
            response_json = response.json()
            assert response_json["detail"] == "Username and password are required"

    @pytest.mark.asyncio
    async def test_registration_with_existing_username(self, valid_user_data):
        async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
            response = await client.post("auth/register/", json=valid_user_data)

            assert response.status_code == 400
            response_json = response.json()
            assert response_json["detail"] == "Username already registered"

    @pytest.mark.asyncio
    async def test_registration_with_unicode(self, unicode_user_data):
        async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
            response = await client.post("auth/register/", json=unicode_user_data)

            assert response.status_code == 400
            response_json = response.json()
            assert response_json["detail"] == "Username and password must contain only English letters, numbers, and underscores"

