"""Tests for GET /api/stories endpoint (list stories).

These tests verify story listing functionality, including:
- Pagination (limit and offset)
- Filtering by category, date range
- Text search (q parameter)
- Ordering (asc/desc by created_at)

Test Setup:
    Tests use centralized fixtures from conftest.py.
    Run tests using the test runner script:
    
        ./scripts/run_tests.ps1  # Windows
        ./scripts/run_tests.sh   # Linux/Mac

Run tests:
    pytest tests/test_list_stories.py -v
"""

from datetime import date, timedelta

import pytest
import pytest_asyncio
from httpx import AsyncClient


# Test Fixtures

@pytest_asyncio.fixture
async def sample_stories(async_client: AsyncClient):
    """Create sample stories for testing.
    
    Creates stories with different categories, dates, and content
    to support various filter tests.
    """
    stories = []
    today = date.today()
    
    # Story 1: Travel category, recent
    story1 = await async_client.post("/api/stories/", json={
        "title": "Amazing Trip to Paris",
        "body": "Visited the Eiffel Tower and Louvre Museum. Incredible experience!",
        "category": "travel",
        "location_lat": 48.8566,
        "location_lng": 2.3522,
        "date_of_story": str(today - timedelta(days=1)),
    })
    if story1.status_code == 201:
        stories.append(story1.json())
    
    # Story 2: Food category, older
    story2 = await async_client.post("/api/stories/", json={
        "title": "Best Ramen in Tokyo",
        "body": "Found an amazing ramen shop in Shibuya.",
        "category": "food",
        "location_lat": 35.6762,
        "location_lng": 139.6503,
        "date_of_story": str(today - timedelta(days=10)),
    })
    if story2.status_code == 201:
        stories.append(story2.json())
    
    # Story 3: Travel category, oldest
    story3 = await async_client.post("/api/stories/", json={
        "title": "Hiking in the Alps",
        "body": "Beautiful mountain views and fresh air.",
        "category": "travel",
        "location_lat": 46.5197,
        "location_lng": 6.6323,
        "date_of_story": str(today - timedelta(days=30)),
    })
    if story3.status_code == 201:
        stories.append(story3.json())
    
    # Story 4: History category, no date
    story4 = await async_client.post("/api/stories/", json={
        "title": "Ancient Rome Tour",
        "body": "Visited the Colosseum and Roman Forum.",
        "category": "history",
        "location_lat": 41.9028,
        "location_lng": 12.4964,
    })
    if story4.status_code == 201:
        stories.append(story4.json())
    
    # Story 5: Nature category with unique keyword
    story5 = await async_client.post("/api/stories/", json={
        "title": "Sunset at Grand Canyon",
        "body": "Breathtaking panoramic sunset views.",
        "category": "nature",
        "location_lat": 36.1069,
        "location_lng": -112.1129,
        "date_of_story": str(today - timedelta(days=5)),
    })
    if story5.status_code == 201:
        stories.append(story5.json())
    
    return stories


# Test Cases

@pytest.mark.asyncio
async def test_list_default_pagination(async_client: AsyncClient):
    """Test listing stories with default pagination parameters."""
    # Act: GET stories with defaults
    response = await async_client.get("/api/stories/")
    
    # Assert: 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    # Assert: Response structure
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    
    # Assert: Default pagination values
    assert data["limit"] == 20  # Default limit
    assert data["offset"] == 0  # Default offset
    
    # Assert: Items is a list
    assert isinstance(data["items"], list)
    
    # Assert: Number of items doesn't exceed limit
    assert len(data["items"]) <= data["limit"]


@pytest.mark.asyncio
async def test_list_custom_limit_offset(async_client: AsyncClient, sample_stories):
    """Test listing with custom limit and offset."""
    # Arrange: Ensure we have at least 3 stories
    assert len(sample_stories) >= 3, "Need at least 3 sample stories"
    
    # Act: GET first page (limit=2, offset=0)
    response1 = await async_client.get("/api/stories/?limit=2&offset=0")
    
    # Assert: First page
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["limit"] == 2
    assert data1["offset"] == 0
    assert len(data1["items"]) <= 2
    
    # Act: GET second page (limit=2, offset=2)
    response2 = await async_client.get("/api/stories/?limit=2&offset=2")
    
    # Assert: Second page
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["limit"] == 2
    assert data2["offset"] == 2
    
    # Assert: Different items on different pages (if enough stories exist)
    if len(data1["items"]) > 0 and len(data2["items"]) > 0:
        first_page_ids = {item["id"] for item in data1["items"]}
        second_page_ids = {item["id"] for item in data2["items"]}
        assert first_page_ids.isdisjoint(second_page_ids), "Pages should not overlap"


@pytest.mark.asyncio
async def test_list_filter_category(async_client: AsyncClient, sample_stories):
    """Test filtering stories by category."""
    # Arrange: We have stories with category='travel'
    travel_count = sum(1 for s in sample_stories if s.get("category") == "travel")
    assert travel_count > 0, "Need at least one travel story"
    
    # Act: Filter by travel category
    response = await async_client.get("/api/stories/?category=travel")
    
    # Assert: 200 OK
    assert response.status_code == 200
    
    # Assert: All returned stories have travel category
    data = response.json()
    assert len(data["items"]) > 0, "Should return at least one travel story"
    
    for item in data["items"]:
        assert item["category"] == "travel", f"Expected category 'travel', got '{item['category']}'"


@pytest.mark.asyncio
async def test_list_filter_category_no_results(async_client: AsyncClient, sample_stories):
    """Test filtering by category with no matching stories."""
    # Act: Filter by a category that doesn't exist
    response = await async_client.get("/api/stories/?category=nonexistent")
    
    # Assert: 200 OK with empty results
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_date_range_from(async_client: AsyncClient, sample_stories):
    """Test filtering stories by date_from."""
    # Arrange: Get a reference date (5 days ago)
    from_date = date.today() - timedelta(days=7)
    
    # Act: Filter stories from 7 days ago onwards
    response = await async_client.get(f"/api/stories/?date_from={from_date}")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: All returned stories have date >= date_from (or null)
    for item in data["items"]:
        if item["date_of_story"]:
            story_date = date.fromisoformat(item["date_of_story"])
            assert story_date >= from_date, f"Story date {story_date} should be >= {from_date}"


@pytest.mark.asyncio
async def test_list_date_range_to(async_client: AsyncClient, sample_stories):
    """Test filtering stories by date_to."""
    # Arrange: Get a reference date (5 days ago)
    to_date = date.today() - timedelta(days=5)
    
    # Act: Filter stories up to 5 days ago
    response = await async_client.get(f"/api/stories/?date_to={to_date}")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: All returned stories have date <= date_to (or null)
    for item in data["items"]:
        if item["date_of_story"]:
            story_date = date.fromisoformat(item["date_of_story"])
            assert story_date <= to_date, f"Story date {story_date} should be <= {to_date}"


@pytest.mark.asyncio
async def test_list_date_range_both(async_client: AsyncClient, sample_stories):
    """Test filtering stories by both date_from and date_to."""
    # Arrange: Date range (20 days ago to 2 days ago)
    from_date = date.today() - timedelta(days=20)
    to_date = date.today() - timedelta(days=2)
    
    # Act: Filter with date range
    response = await async_client.get(f"/api/stories/?date_from={from_date}&date_to={to_date}")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: All returned stories are within range
    for item in data["items"]:
        if item["date_of_story"]:
            story_date = date.fromisoformat(item["date_of_story"])
            assert from_date <= story_date <= to_date, \
                f"Story date {story_date} should be between {from_date} and {to_date}"


@pytest.mark.asyncio
async def test_list_search_q_title(async_client: AsyncClient, sample_stories):
    """Test text search in story titles."""
    # Act: Search for "Paris" in title
    response = await async_client.get("/api/stories/?q=Paris")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: At least one result
    assert len(data["items"]) > 0, "Should find story with 'Paris' in title"
    
    # Assert: Results contain the search term in title or body
    found = False
    for item in data["items"]:
        if "paris" in item["title"].lower() or (item["body"] and "paris" in item["body"].lower()):
            found = True
            break
    assert found, "At least one result should contain 'Paris'"


@pytest.mark.asyncio
async def test_list_search_q_body(async_client: AsyncClient, sample_stories):
    """Test text search in story body."""
    # Act: Search for "Louvre" (appears in body)
    response = await async_client.get("/api/stories/?q=Louvre")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: At least one result
    assert len(data["items"]) > 0, "Should find story with 'Louvre' in body"
    
    # Assert: Results contain the search term
    found = False
    for item in data["items"]:
        if item["body"] and "louvre" in item["body"].lower():
            found = True
            break
    assert found, "At least one result should contain 'Louvre' in body"


@pytest.mark.asyncio
async def test_list_search_q_case_insensitive(async_client: AsyncClient, sample_stories):
    """Test that text search is case-insensitive."""
    # Act: Search with different cases
    response1 = await async_client.get("/api/stories/?q=PARIS")
    response2 = await async_client.get("/api/stories/?q=paris")
    response3 = await async_client.get("/api/stories/?q=PaRiS")
    
    # Assert: All should return the same results
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    
    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()
    
    # Same number of results
    assert len(data1["items"]) == len(data2["items"]) == len(data3["items"])


@pytest.mark.asyncio
async def test_list_search_q_no_results(async_client: AsyncClient, sample_stories):
    """Test text search with no matching results."""
    # Act: Search for something that doesn't exist
    response = await async_client.get("/api/stories/?q=xyzabc123nonexistent")
    
    # Assert: 200 OK with empty results
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_ordering_desc_default(async_client: AsyncClient, sample_stories):
    """Test default ordering (created_at DESC - newest first)."""
    # Arrange: Ensure we have multiple stories
    assert len(sample_stories) >= 2, "Need at least 2 stories"
    
    # Act: GET without order parameter (should default to desc)
    response = await async_client.get("/api/stories/")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: Stories are ordered by created_at descending
    if len(data["items"]) >= 2:
        for i in range(len(data["items"]) - 1):
            current_time = data["items"][i]["created_at"]
            next_time = data["items"][i + 1]["created_at"]
            assert current_time >= next_time, \
                f"Stories should be ordered newest first (DESC): {current_time} >= {next_time}"


@pytest.mark.asyncio
async def test_list_ordering_asc(async_client: AsyncClient, sample_stories):
    """Test ascending order (created_at ASC - oldest first)."""
    # Arrange: Ensure we have multiple stories
    assert len(sample_stories) >= 2, "Need at least 2 stories"
    
    # Act: GET with order=asc
    response = await async_client.get("/api/stories/?order=asc")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: Stories are ordered by created_at ascending
    if len(data["items"]) >= 2:
        for i in range(len(data["items"]) - 1):
            current_time = data["items"][i]["created_at"]
            next_time = data["items"][i + 1]["created_at"]
            assert current_time <= next_time, \
                f"Stories should be ordered oldest first (ASC): {current_time} <= {next_time}"


@pytest.mark.asyncio
async def test_list_ordering_explicit_desc(async_client: AsyncClient, sample_stories):
    """Test explicit descending order."""
    # Act: GET with order=desc
    response = await async_client.get("/api/stories/?order=desc")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: Stories are ordered descending
    if len(data["items"]) >= 2:
        for i in range(len(data["items"]) - 1):
            current_time = data["items"][i]["created_at"]
            next_time = data["items"][i + 1]["created_at"]
            assert current_time >= next_time


@pytest.mark.asyncio
async def test_list_combined_filters(async_client: AsyncClient, sample_stories):
    """Test combining multiple filters (category + date + search)."""
    # Act: Combine category and search
    response = await async_client.get("/api/stories/?category=travel&q=Paris")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: Results match all criteria
    for item in data["items"]:
        assert item["category"] == "travel"
        # Should contain 'Paris' in title or body
        text_matches = (
            "paris" in item["title"].lower() or
            (item["body"] and "paris" in item["body"].lower())
        )
        assert text_matches


@pytest.mark.asyncio
async def test_list_limit_bounds(async_client: AsyncClient):
    """Test limit parameter bounds validation."""
    # Act: Test with limit=0 (should be rejected or adjusted)
    response1 = await async_client.get("/api/stories/?limit=0")
    # Should either be 422 (validation error) or adjusted to minimum
    assert response1.status_code in [200, 422]
    
    # Act: Test with limit=101 (exceeds max of 100)
    response2 = await async_client.get("/api/stories/?limit=101")
    # Should either be 422 or capped at 100
    assert response2.status_code in [200, 422]
    if response2.status_code == 200:
        data = response2.json()
        assert data["limit"] <= 100


@pytest.mark.asyncio
async def test_list_offset_negative(async_client: AsyncClient):
    """Test that negative offset is rejected."""
    # Act: Try negative offset
    response = await async_client.get("/api/stories/?offset=-1")
    
    # Assert: Should be rejected with 422
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_empty_database(async_client: AsyncClient):
    """Test listing when no stories match filters."""
    # Act: Use a very restrictive date range
    response = await async_client.get("/api/stories/?date_from=1900-01-01&date_to=1900-01-02")
    
    # Assert: 200 OK with empty results
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["limit"] == 20
    assert data["offset"] == 0


@pytest.mark.asyncio
async def test_list_response_structure(async_client: AsyncClient):
    """Test that response includes all required fields."""
    # Act: GET stories
    response = await async_client.get("/api/stories/")
    
    # Assert: 200 OK
    assert response.status_code == 200
    data = response.json()
    
    # Assert: Required fields exist
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    
    # Assert: Each item has StoryRead structure
    if len(data["items"]) > 0:
        item = data["items"][0]
        required_fields = ["id", "title", "location_lat", "location_lng", "created_at", "updated_at"]
        for field in required_fields:
            assert field in item, f"Item should have '{field}' field"
