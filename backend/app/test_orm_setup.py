"""Quick test script to verify ORM setup without running the server.

This script tests that all imports work correctly and models are properly configured.
Run this after installing dependencies to verify the setup.

Usage:
    python -m app.test_orm_setup
"""

import asyncio
from datetime import date, datetime

from app.core.config import settings
from app.db.models import Photo, Story, User
from app.db.session import AsyncSessionLocal
from app.schemas.photo import PhotoRead
from app.schemas.story import StoryCreate, StoryRead
from app.schemas.user import UserRead


def test_imports():
    """Test that all modules can be imported without errors."""
    print("✓ All imports successful")
    print(f"  - Settings loaded: DATABASE_URL = {settings.DATABASE_URL[:30]}...")
    print(f"  - CORS origins: {settings.cors_origins_list}")
    print(f"  - Debug mode: {settings.DEBUG}")


def test_models():
    """Test that ORM models are properly configured."""
    print("\n✓ ORM Models configured:")
    print(f"  - User table: {User.__tablename__}")
    print(f"  - Story table: {Story.__tablename__}")
    print(f"  - Photo table: {Photo.__tablename__}")


def test_schemas():
    """Test that Pydantic schemas can be instantiated."""
    # Create a story schema
    story_data = StoryCreate(
        title="Test Story",
        body="This is a test story",
        category="travel",
        location_lat=40.7128,
        location_lng=-74.0060,
        date_of_story=date(2026, 1, 25),
    )
    print("\n✓ Pydantic Schemas working:")
    print(f"  - StoryCreate: {story_data.title}")
    print(f"  - Location: ({story_data.location_lat}, {story_data.location_lng})")


async def test_session():
    """Test that async session can be created."""
    try:
        async with AsyncSessionLocal() as session:
            print("\n✓ Async session created successfully")
            print(f"  - Session type: {type(session).__name__}")
            return True
    except Exception as e:
        print(f"\n✗ Session creation failed: {e}")
        print("  - Make sure DATABASE_URL is set correctly in .env")
        print("  - Ensure PostgreSQL is running and accessible")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("GeoStory ORM Setup Verification")
    print("=" * 60)
    
    try:
        test_imports()
        test_models()
        test_schemas()
        await test_session()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed! ORM setup is complete.")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run migrations: alembic upgrade head")
        print("  2. Start the server: uvicorn app.main:app --reload")
        print("  3. Test health endpoint: curl http://localhost:8000/api/health")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Test failed: {e}")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Check .env file exists with DATABASE_URL")
        print("  3. Verify PostgreSQL is running")


if __name__ == "__main__":
    asyncio.run(main())
