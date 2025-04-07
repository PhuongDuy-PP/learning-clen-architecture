import pytest
import pytest_asyncio
from app import create_app
import json
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from application.interfaces.logger import Logger
from application.interfaces.validator import Validator
from application.dtos.user_dto import UserInputDTO

class MockLogger(Logger):
    def info(self, message: str) -> None:
        pass
    
    def error(self, message: str) -> None:
        pass
    
    def warning(self, message: str) -> None:
        pass
    
    def debug(self, message: str) -> None:
        pass

class MockValidator(Validator):
    def validate_user_input(self, user_input: UserInputDTO) -> None:
        # Basic validation for testing
        if not user_input.email or not user_input.username or not user_input.password:
            raise ValueError("Missing required fields")
        pass

@pytest_asyncio.fixture(scope="function")
async def client():
    app = create_app()
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

@pytest.mark.asyncio
async def test_register_user_success(client):
    # Test data
    test_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    # Make request
    response = await client.post('/api/users/register',
                         json=test_data)
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['username'] == test_data['username']
    assert data['data']['email'] == test_data['email']

@pytest.mark.asyncio
async def test_register_user_missing_fields(client):
    # Test data with missing fields
    test_data = {
        "username": "testuser",
        # email is missing
        "password": "password123"
    }
    
    # Make request
    response = await client.post('/api/users/register',
                         json=test_data)
    
    # Assertions
    assert response.status_code == 400
    data = response.json()
    assert data['success'] is False
    assert data['message'] == 'Missing required fields'

@pytest.mark.asyncio
async def test_list_users(client):
    response = await client.get('/api/users')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get('/api/users/nonexistent-id')
    assert response.status_code == 404
    data = response.json()
    assert data['success'] is False 