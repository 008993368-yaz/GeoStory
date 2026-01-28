"""Pytest configuration and fixtures for backend tests.

This module provides shared fixtures for all tests, including:
- Test database setup and teardown
- Async HTTP client
- Database session management
- Cleanup between tests
"""

import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.deps import get_db


# Test Database Configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://geostory_user:geostory_pass@localhost:5433/geostory_test"
)

# Create test engine and session factory
# Use NullPool to avoid connection issues between tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,  # Don't pool connections - avoids "Event loop is closed" errors
)


# Database Fixtures

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a test database session.
    
    This fixture:
    - Creates a new session for each test
    - Cleans up the database after each test
    - Ensures isolation between tests
    """
    # Create a fresh session for each test
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        yield session
        
        # Cleanup: Truncate all tables after each test to ensure isolation
        try:
            await session.execute(text("TRUNCATE TABLE photos, stories, users RESTART IDENTITY CASCADE"))
            await session.commit()
        except Exception:
            await session.rollback()


@pytest_asyncio.fixture
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client with database dependency override.
    
    This fixture:
    - Creates an AsyncClient for making HTTP requests to the app
    - Overrides the get_db dependency to use the test database
    - Ensures all requests use the test database session
    """
    
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        """Override get_db to use test database."""
        yield db_session
    
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create client
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=False
    ) as client:
        yield client
    
    # Clear overrides
    app.dependency_overrides.clear()


# Helper Fixtures

@pytest.fixture
def sample_story_data() -> dict:
    """Provide sample valid story data for tests."""
    return {
        "title": "A Beautiful Day in San Francisco",
        "body": "Today I visited the Golden Gate Bridge and it was spectacular!",
        "category": "travel",
        "location_lat": 37.8199,
        "location_lng": -122.4783,
        "date_of_story": "2026-01-15"
    }


@pytest.fixture
def sample_invalid_coordinates() -> list[dict]:
    """Provide sample invalid coordinate data for validation tests."""
    return [
        {"lat": 91.0, "lng": 0.0, "reason": "latitude > 90"},
        {"lat": -91.0, "lng": 0.0, "reason": "latitude < -90"},
        {"lat": 0.0, "lng": 181.0, "reason": "longitude > 180"},
        {"lat": 0.0, "lng": -181.0, "reason": "longitude < -180"},
    ]
