"""Tests for GET /api/stories/{id} endpoint (get story by ID).

These tests verify single story retrieval functionality, including:
- Successful retrieval by valid UUID
- 404 response for non-existent story
- 422 response for invalid UUID format

Test Setup:
    Tests use centralized fixtures from conftest.py.
    Run tests using the test runner script:
    
        ./scripts/run_tests.ps1  # Windows
        ./scripts/run_tests.sh   # Linux/Mac

Run tests:
    pytest tests/test_get_story.py -v
"""

from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient


# Test Fixtures

@pytest_asyncio.fixture
async def sample_story(async_client: AsyncClient):
    """Create a sample story for testing.
    
    Returns the created story data including its ID.
    """
    story_data = {
        "title": "Test Story for Retrieval",
        "body": "This is a test story created for GET endpoint testing.",
        "category": "travel",
        "location_lat": 40.7128,
        "location_lng": -74.0060,
        "date_of_story": "2026-01-20",
    }
    
    response = await async_client.post("/api/stories/", json=story_data)
    
    # Only return if creation was successful
    if response.status_code == 201:
        return response.json()
    
    return None


# Test Cases

@pytest.mark.asyncio
async def test_get_story_success(async_client: AsyncClient, sample_story):
    """Test successful retrieval of a story by ID."""
    # Arrange: Ensure we have a sample story
    assert sample_story is not None, "Failed to create sample story"
    story_id = sample_story["id"]
    
    # Act: GET story by ID
    response = await async_client.get(f"/api/stories/{story_id}")
    
    # Assert: 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    # Assert: Response structure matches StoryRead
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "location_lat" in data
    assert "location_lng" in data
    
    # Assert: Data matches created story
    assert data["id"] == story_id
    assert data["title"] == sample_story["title"]
    assert data["body"] == sample_story["body"]
    assert data["category"] == sample_story["category"]
    assert data["location_lat"] == sample_story["location_lat"]
    assert data["location_lng"] == sample_story["location_lng"]
    
    # Assert: Photos list exists (empty for new story)
    assert "photos" in data
    assert isinstance(data["photos"], list)


@pytest.mark.asyncio
async def test_get_story_includes_all_fields(async_client: AsyncClient, sample_story):
    """Test that retrieved story includes all expected fields."""
    # Arrange
    assert sample_story is not None
    story_id = sample_story["id"]
    
    # Act
    response = await async_client.get(f"/api/stories/{story_id}")
    
    # Assert: 200 OK
    assert response.status_code == 200
    
    # Assert: All required fields present
    data = response.json()
    required_fields = [
        "id", "owner_id", "title", "body", "category",
        "location_lat", "location_lng", "date_of_story",
        "created_at", "updated_at", "photos"
    ]
    
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


@pytest.mark.asyncio
async def test_get_story_not_found(async_client: AsyncClient):
    """Test that getting a non-existent story returns 404."""
    # Arrange: Generate a random UUID that doesn't exist
    nonexistent_id = uuid4()
    
    # Act: Try to GET non-existent story
    response = await async_client.get(f"/api/stories/{nonexistent_id}")
    
    # Assert: 404 Not Found
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    # Assert: Error message
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


@pytest.mark.asyncio
async def test_get_story_invalid_uuid(async_client: AsyncClient):
    """Test that invalid UUID format returns 422."""
    # Arrange: Use an invalid UUID string
    invalid_uuid = "not-a-valid-uuid"
    
    # Act: Try to GET with invalid UUID
    response = await async_client.get(f"/api/stories/{invalid_uuid}")
    
    # Assert: 422 Unprocessable Entity (FastAPI validation error)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    
    # Assert: Error details mention validation
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_get_story_invalid_uuid_format_variations(async_client: AsyncClient):
    """Test various invalid UUID formats all return 422."""
    invalid_uuids = [
        "123",
        "abc-def",
        "not-a-uuid",
        "12345678-1234-1234-1234",  # Too short
        "12345678-1234-1234-1234-1234567890123",  # Too long
    ]
    
    for invalid_uuid in invalid_uuids:
        # Act
        response = await async_client.get(f"/api/stories/{invalid_uuid}")
        
        # Assert: All should return 422
        assert response.status_code == 422, \
            f"Invalid UUID '{invalid_uuid}' should return 422, got {response.status_code}"


@pytest.mark.asyncio
async def test_get_story_preserves_null_fields(async_client: AsyncClient):
    """Test that stories with null optional fields are returned correctly."""
    # Arrange: Create a minimal story (only required fields)
    minimal_story_data = {
        "title": "Minimal Story",
        "location_lat": 0.0,
        "location_lng": 0.0,
    }
    
    create_response = await async_client.post("/api/stories/", json=minimal_story_data)
    if create_response.status_code != 201:
        pytest.skip("Could not create minimal story (DB not available)")
    
    story_id = create_response.json()["id"]
    
    # Act: GET the minimal story
    response = await async_client.get(f"/api/stories/{story_id}")
    
    # Assert: 200 OK
    assert response.status_code == 200
    
    # Assert: Optional fields are null
    data = response.json()
    assert data["body"] is None or data["body"] == ""
    assert data["category"] is None
    assert data["date_of_story"] is None
    assert data["owner_id"] is None


@pytest.mark.asyncio
async def test_get_story_multiple_retrievals_consistent(async_client: AsyncClient, sample_story):
    """Test that retrieving the same story multiple times returns consistent data."""
    # Arrange
    assert sample_story is not None
    story_id = sample_story["id"]
    
    # Act: GET the same story twice
    response1 = await async_client.get(f"/api/stories/{story_id}")
    response2 = await async_client.get(f"/api/stories/{story_id}")
    
    # Assert: Both successful
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Assert: Data is identical
    data1 = response1.json()
    data2 = response2.json()
    
    assert data1["id"] == data2["id"]
    assert data1["title"] == data2["title"]
    assert data1["created_at"] == data2["created_at"]
    assert data1["updated_at"] == data2["updated_at"]


@pytest.mark.asyncio
async def test_get_story_with_different_categories(async_client: AsyncClient):
    """Test retrieving stories with different categories."""
    # Arrange: Create stories with different categories
    categories = ["travel", "food", "history"]
    story_ids = []
    
    for category in categories:
        story_data = {
            "title": f"Story about {category}",
            "category": category,
            "location_lat": 0.0,
            "location_lng": 0.0,
        }
        create_response = await async_client.post("/api/stories/", json=story_data)
        if create_response.status_code == 201:
            story_ids.append((create_response.json()["id"], category))
    
    # Skip if DB not available
    if not story_ids:
        pytest.skip("Could not create stories (DB not available)")
    
    # Act & Assert: GET each story and verify category
    for story_id, expected_category in story_ids:
        response = await async_client.get(f"/api/stories/{story_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == expected_category


@pytest.mark.asyncio
async def test_get_story_response_matches_create_response(async_client: AsyncClient):
    """Test that GET response matches the POST response (except timestamps may differ slightly)."""
    # Arrange: Create a story
    story_data = {
        "title": "Consistency Test Story",
        "body": "Testing response consistency",
        "category": "travel",
        "location_lat": 35.6762,
        "location_lng": 139.6503,
        "date_of_story": "2026-01-15",
    }
    
    create_response = await async_client.post("/api/stories/", json=story_data)
    if create_response.status_code != 201:
        pytest.skip("Could not create story (DB not available)")
    
    created_data = create_response.json()
    story_id = created_data["id"]
    
    # Act: GET the story
    get_response = await async_client.get(f"/api/stories/{story_id}")
    
    # Assert: 200 OK
    assert get_response.status_code == 200
    
    # Assert: Core fields match
    retrieved_data = get_response.json()
    assert retrieved_data["id"] == created_data["id"]
    assert retrieved_data["title"] == created_data["title"]
    assert retrieved_data["body"] == created_data["body"]
    assert retrieved_data["category"] == created_data["category"]
    assert retrieved_data["location_lat"] == created_data["location_lat"]
    assert retrieved_data["location_lng"] == created_data["location_lng"]
    assert retrieved_data["date_of_story"] == created_data["date_of_story"]
