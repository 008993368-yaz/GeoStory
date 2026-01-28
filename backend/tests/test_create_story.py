"""Tests for POST /api/stories endpoint.

These tests verify story creation functionality, including:
- Successful story creation with valid data
- Validation errors for invalid coordinates
- Validation errors for invalid categories
- Anonymous vs. attributed story creation

Test Setup:
    Tests use centralized fixtures from conftest.py.
    Run tests using the test runner script:
    
        ./scripts/run_tests.ps1  # Windows
        ./scripts/run_tests.sh   # Linux/Mac

Run tests:
    pytest tests/test_create_story.py -v
"""

import pytest
from httpx import AsyncClient


# Test Cases

@pytest.mark.asyncio
async def test_create_story_success(async_client: AsyncClient):
    """Test successful story creation with valid data."""
    # Arrange: Valid story payload
    story_data = {
        "title": "Beautiful Sunset at the Beach",
        "body": "I watched the most amazing sunset today at Venice Beach. The colors were incredible!",
        "category": "travel",
        "location_lat": 33.9850,
        "location_lng": -118.4695,
        "date_of_story": "2026-01-20",
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 201 Created
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    
    # Assert: Response matches StoryRead schema
    data = response.json()
    assert "id" in data, "Response must include 'id'"
    assert "created_at" in data, "Response must include 'created_at'"
    assert "updated_at" in data, "Response must include 'updated_at'"
    
    # Assert: Response includes submitted data
    assert data["title"] == story_data["title"]
    assert data["body"] == story_data["body"]
    assert data["category"] == story_data["category"]
    assert data["location_lat"] == story_data["location_lat"]
    assert data["location_lng"] == story_data["location_lng"]
    assert data["date_of_story"] == story_data["date_of_story"]
    
    # Assert: Anonymous story (no owner_id)
    assert data["owner_id"] is None
    
    # Assert: Photos list exists (empty for new story)
    assert "photos" in data
    assert data["photos"] == []


@pytest.mark.asyncio
async def test_create_story_minimal(async_client: AsyncClient):
    """Test story creation with only required fields."""
    # Arrange: Minimal valid payload (title + coordinates)
    story_data = {
        "title": "Quick Note",
        "location_lat": 0.0,
        "location_lng": 0.0,
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 201 Created
    assert response.status_code == 201
    
    # Assert: Optional fields are null
    data = response.json()
    assert data["body"] is None
    assert data["category"] is None
    assert data["date_of_story"] is None


@pytest.mark.asyncio
async def test_create_story_invalid_lat_too_high(async_client: AsyncClient):
    """Test story creation fails with latitude > 90."""
    # Arrange: Invalid latitude
    story_data = {
        "title": "Invalid Location",
        "location_lat": 100.0,  # Invalid: > 90
        "location_lng": 0.0,
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 422 Unprocessable Entity (Pydantic validation)
    assert response.status_code == 422
    
    # Assert: Error details mention latitude
    data = response.json()
    assert "detail" in data
    error_msg = str(data["detail"]).lower()
    assert "location_lat" in error_msg or "latitude" in error_msg


@pytest.mark.asyncio
async def test_create_story_invalid_lat_too_low(async_client: AsyncClient):
    """Test story creation fails with latitude < -90."""
    # Arrange: Invalid latitude
    story_data = {
        "title": "Invalid Location",
        "location_lat": -95.0,  # Invalid: < -90
        "location_lng": 0.0,
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 422 Unprocessable Entity
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_story_invalid_lng_too_high(async_client: AsyncClient):
    """Test story creation fails with longitude > 180."""
    # Arrange: Invalid longitude
    story_data = {
        "title": "Invalid Location",
        "location_lat": 0.0,
        "location_lng": 200.0,  # Invalid: > 180
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 422 Unprocessable Entity
    assert response.status_code == 422
    
    # Assert: Error details mention longitude
    data = response.json()
    error_msg = str(data["detail"]).lower()
    assert "location_lng" in error_msg or "longitude" in error_msg


@pytest.mark.asyncio
async def test_create_story_invalid_category(async_client: AsyncClient):
    """Test story creation fails with invalid category."""
    # Arrange: Invalid category
    story_data = {
        "title": "Test Story",
        "category": "invalid_category",  # Not in StoryCategory enum
        "location_lat": 0.0,
        "location_lng": 0.0,
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 422 Unprocessable Entity (Pydantic validates category as Literal)
    assert response.status_code == 422
    
    # Assert: Error mentions category
    data = response.json()
    error_msg = str(data["detail"]).lower()
    assert "category" in error_msg


@pytest.mark.asyncio
async def test_create_story_missing_required_field(async_client: AsyncClient):
    """Test story creation fails when missing required field."""
    # Arrange: Missing title (required field)
    story_data = {
        "body": "This story has no title",
        "location_lat": 0.0,
        "location_lng": 0.0,
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 422 Unprocessable Entity
    assert response.status_code == 422
    
    # Assert: Error mentions missing field
    data = response.json()
    error_msg = str(data["detail"]).lower()
    assert "title" in error_msg


@pytest.mark.asyncio
async def test_create_story_future_date(async_client: AsyncClient):
    """Test story creation fails with future date."""
    # Arrange: Future date (validator should reject)
    story_data = {
        "title": "Time Travel Story",
        "location_lat": 0.0,
        "location_lng": 0.0,
        "date_of_story": "2030-12-31",  # Far future date
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 422 Unprocessable Entity (Pydantic validator)
    assert response.status_code == 422
    
    # Assert: Error mentions date or future
    data = response.json()
    error_msg = str(data["detail"]).lower()
    assert "date" in error_msg or "future" in error_msg


@pytest.mark.asyncio
async def test_create_story_title_too_long(async_client: AsyncClient):
    """Test story creation fails with title exceeding max length."""
    # Arrange: Title > 500 characters
    long_title = "A" * 501
    story_data = {
        "title": long_title,
        "location_lat": 0.0,
        "location_lng": 0.0,
    }
    
    # Act: POST to /api/stories
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Assert: 422 Unprocessable Entity
    assert response.status_code == 422
    
    # Assert: Error mentions title or length
    data = response.json()
    error_msg = str(data["detail"]).lower()
    assert "title" in error_msg


@pytest.mark.asyncio
async def test_create_story_boundary_coordinates(async_client: AsyncClient):
    """Test story creation succeeds with boundary coordinate values."""
    # Arrange: Boundary values (should be valid)
    test_cases = [
        {"location_lat": 90.0, "location_lng": 180.0},   # Max values
        {"location_lat": -90.0, "location_lng": -180.0}, # Min values
        {"location_lat": 0.0, "location_lng": 0.0},      # Equator/Prime meridian
    ]
    
    for coords in test_cases:
        story_data = {
            "title": f"Boundary Test: {coords}",
            **coords,
        }
        
        # Act: POST to /api/stories/
        response = await async_client.post("/api/stories/", json=story_data)
        
        # Assert: 201 Created
        assert response.status_code == 201, f"Boundary test failed for {coords}: {response.text}"
        
        # Assert: Coordinates match
        data = response.json()
        assert data["location_lat"] == coords["location_lat"]
        assert data["location_lng"] == coords["location_lng"]
