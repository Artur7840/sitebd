import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/events/", json={
            "name": "Test Event",
            "event_type": "Seminar",
            "description": "Test description",
            "status": "planning",
            "budget": 1000
        })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"
    assert "id" in data