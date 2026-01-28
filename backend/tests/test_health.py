"""Tests for health check endpoint.

These tests verify the /api/health endpoint returns correct status.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Test health check endpoint returns 200 with correct status."""
    # Act: Request health endpoint
    response = await async_client.get("/api/health")
    
    # Assert: Response is correct
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_check_content_type(async_client: AsyncClient):
    """Test health check returns JSON content type."""
    # Act: Request health endpoint
    response = await async_client.get("/api/health")
    
    # Assert: Content type is JSON
    assert response.status_code == 200
    assert "application/json" in response.headers.get("content-type", "")
