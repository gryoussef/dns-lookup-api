import pytest
from httpx import AsyncClient
from src.main import app, get_database,get_utils
from mock_database import MockDatabase
from src.utils import Utils

# Override dependencies for all tests
@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_database] = lambda: MockDatabase()
    app.dependency_overrides[get_utils] = lambda: Utils()

@pytest.mark.asyncio
async def test_lookup():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/tools/lookup", json={"domain": "example.com"})
    assert response.status_code == 200
    assert "ip_addresses" in response.json()

@pytest.mark.asyncio
async def test_lookup_invalid_domain():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/tools/lookup", json={"domain": "invalid_domain"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Domain not found"}

@pytest.mark.asyncio
async def test_validate():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/tools/validate", json={"ip": "127.0.0.1"})
    assert response.status_code == 200
    assert response.json() == {"is_valid": True}

@pytest.mark.asyncio
async def test_validate_invalid_ip():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/tools/validate", json={"ip": "invalid_ip"})
    assert response.status_code == 200
    assert response.json() == {"is_valid": False}