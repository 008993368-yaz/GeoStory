"""CRUD operations for Story model.

This module contains database operations for creating, reading, updating,
and deleting Story records.
"""

from datetime import date
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import func, or_, select
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


async def list_stories(
    db: AsyncSession,
    *,
    limit: int = 20,
    offset: int = 0,
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    q: Optional[str] = None,
    order: str = "desc",
) -> Tuple[List[Story], int]:
    """List stories with filtering, pagination, and ordering.
    
    Args:
        db: Async database session
        limit: Maximum number of stories to return (capped at 100)
        offset: Number of stories to skip for pagination
        category: Filter by exact category match (optional)
        date_from: Filter stories from this date onwards (optional)
        date_to: Filter stories up to this date (optional)
        q: Text search query for title/body (case-insensitive, optional)
        order: Sort order for created_at ("asc" or "desc", default "desc")
        
    Returns:
        Tuple[List[Story], int]: (list of Story ORM objects, total count)
        
    Example:
        stories, total = await list_stories(
            db,
            limit=10,
            category="travel",
            q="paris",
            order="desc"
        )
    """
    # Cap limit to prevent huge responses
    limit = min(limit, 100)
    
    # Build base query
    stmt = select(Story)
    
    # Apply filters
    filters = []
    
    if category:
        filters.append(Story.category == category)
    
    if date_from:
        filters.append(Story.date_of_story >= date_from)
    
    if date_to:
        filters.append(Story.date_of_story <= date_to)
    
    if q:
        # Case-insensitive search on title OR body
        # Use ilike for PostgreSQL (safe from SQL injection via parameter binding)
        search_pattern = f"%{q}%"
        filters.append(
            or_(
                Story.title.ilike(search_pattern),
                Story.body.ilike(search_pattern),
            )
        )
    
    # Apply all filters to the query
    if filters:
        stmt = stmt.where(*filters)
    
    # Count total matching records (before pagination)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    count_result = await db.execute(count_stmt)
    total = count_result.scalar() or 0
    
    # Apply ordering
    if order.lower() == "asc":
        stmt = stmt.order_by(Story.created_at.asc())
    else:
        stmt = stmt.order_by(Story.created_at.desc())
    
    # Apply pagination
    stmt = stmt.limit(limit).offset(offset)
    
    # Execute query and get results
    result = await db.execute(stmt)
    stories = result.scalars().all()
    
    return list(stories), total
