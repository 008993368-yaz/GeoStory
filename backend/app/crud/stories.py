"""CRUD operations for Story model.

This module contains database operations for creating, reading, updating,
and deleting Story records. Currently implements only create functionality.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Story
from app.schemas.story import StoryCreate


async def create_story(
    db: AsyncSession,
    story_in: StoryCreate,
    owner_id: Optional[UUID] = None,
) -> Story:
    """Create a new story in the database.
    
    Args:
        db: Async database session
        story_in: Pydantic schema with validated story data
        owner_id: UUID of the story owner (None for anonymous stories)
        
    Returns:
        Story: Created Story ORM instance with DB-generated fields (id, timestamps)
        
    Example:
        story_data = StoryCreate(
            title="My Trip to Paris",
            body="An amazing journey...",
            category="travel",
            location_lat=48.8566,
            location_lng=2.3522,
        )
        story = await create_story(db, story_data, owner_id=some_uuid)
    """
    # Map Pydantic schema fields to ORM model fields
    story_dict = story_in.model_dump()
    
    # Create ORM instance
    db_story = Story(
        owner_id=owner_id,
        title=story_dict["title"],
        body=story_dict.get("body"),
        category=story_dict.get("category"),
        location_lat=story_dict["location_lat"],
        location_lng=story_dict["location_lng"],
        date_of_story=story_dict.get("date_of_story"),
    )
    
    # Add to session and flush to get DB-generated values
    db.add(db_story)
    await db.commit()
    
    # Refresh to load server-default fields (id, created_at, updated_at)
    await db.refresh(db_story)
    
    return db_story
