"""Story API routes.

This module defines the FastAPI router for story-related endpoints.
Implements POST and GET endpoints for story creation and listing.
"""

from datetime import date
from typing import Literal, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.stories import create_story, list_stories
from app.deps import get_db
from app.schemas.story import StoryCreate, StoryList, StoryRead


# Router configuration
router = APIRouter(
    prefix="/api/stories",
    tags=["stories"],
)


@router.post(
    "/",
    response_model=StoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new story",
    description="Create a new location-based story. Stories can be anonymous (no owner) or attributed to a user.",
)
async def create_story_endpoint(
    story_in: StoryCreate,
    db: AsyncSession = Depends(get_db),
    x_owner_id: Optional[str] = Header(None, description="Optional owner UUID"),
) -> StoryRead:
    """Create a new story.
    
    Args:
        story_in: Story data (validated by Pydantic)
        db: Database session (injected)
        x_owner_id: Optional header with owner UUID for attribution
        
    Returns:
        StoryRead: Created story with id, timestamps, and all fields
        
    Raises:
        HTTPException 400: Database validation error (e.g., constraint violation)
        HTTPException 422: Pydantic validation error (automatic)
        HTTPException 500: Unexpected server error
        
    Example:
        POST /api/stories
        Headers: X-Owner-Id: 123e4567-e89b-12d3-a456-426614174000
        Body: {
            "title": "Sunset at Golden Gate",
            "body": "Beautiful evening...",
            "category": "travel",
            "location_lat": 37.8199,
            "location_lng": -122.4783,
            "date_of_story": "2026-01-20"
        }
    """
    # Parse owner_id from header if provided
    owner_id: Optional[UUID] = None
    if x_owner_id:
        try:
            owner_id = UUID(x_owner_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid owner_id format. Must be a valid UUID.",
            )
    
    try:
        # Create story in database
        db_story = await create_story(db=db, story_in=story_in, owner_id=owner_id)
        
        # Convert ORM model to Pydantic response
        return StoryRead.model_validate(db_story)
        
    except IntegrityError as e:
        # Database constraint violation (e.g., foreign key, check constraint)
        await db.rollback()
        
        # Extract a user-friendly error message
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        
        # Provide specific feedback for common constraint violations
        if "stories_category_check" in error_msg:
            detail = "Validation failed: Invalid category value"
        elif "stories_location_lat_check" in error_msg:
            detail = "Validation failed: Latitude must be between -90 and 90"
        elif "stories_location_lng_check" in error_msg:
            detail = "Validation failed: Longitude must be between -180 and 180"
        elif "fk_stories_owner_id" in error_msg or "users" in error_msg:
            detail = "Validation failed: Owner does not exist"
        else:
            detail = f"Validation failed: Database constraint violation"
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
        
    except DataError as e:
        # Data type errors (e.g., invalid UUID format, numeric overflow)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation failed: Invalid data format - {str(e.orig) if hasattr(e, 'orig') else str(e)}",
        )
        
    except Exception as e:
        # Unexpected errors - log and return 500
        await db.rollback()
        # In production, log this error properly
        # logger.error(f"Unexpected error creating story: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the story",
        )


@router.get(
    "/",
    response_model=StoryList,
    status_code=status.HTTP_200_OK,
    summary="List stories with filters and pagination",
    description="Retrieve a paginated list of stories with optional filtering by category, date range, and text search.",
)
async def list_stories_endpoint(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Maximum number of stories to return (1-100)"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of stories to skip for pagination"
    ),
    category: Optional[str] = Query(
        None,
        description="Filter by story category (exact match)"
    ),
    date_from: Optional[date] = Query(
        None,
        description="Filter stories from this date onwards (inclusive)"
    ),
    date_to: Optional[date] = Query(
        None,
        description="Filter stories up to this date (inclusive)"
    ),
    q: Optional[str] = Query(
        None,
        description="Search query for title or body (case-insensitive)"
    ),
    order: Literal["asc", "desc"] = Query(
        "desc",
        description="Sort order by created_at timestamp"
    ),
) -> StoryList:
    """List stories with filtering, pagination, and ordering.
    
    Args:
        db: Database session (injected)
        limit: Maximum stories per page (default 20, max 100)
        offset: Number of stories to skip (default 0)
        category: Filter by category (optional)
        date_from: Filter stories from this date (optional)
        date_to: Filter stories up to this date (optional)
        q: Text search in title/body (optional)
        order: Sort order - "asc" or "desc" (default "desc")
        
    Returns:
        StoryList: Paginated list with items, total count, and pagination metadata
        
    Example:
        GET /api/stories?limit=10&category=travel&q=paris&order=desc
    """
    try:
        # Fetch stories from database
        items, total = await list_stories(
            db,
            limit=limit,
            offset=offset,
            category=category,
            date_from=date_from,
            date_to=date_to,
            q=q,
            order=order,
        )
        
        # Build response with pagination metadata
        return StoryList(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )
        
    except Exception as e:
        # Unexpected errors
        # In production, log this error properly
        # logger.error(f"Unexpected error listing stories: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while listing stories",
        )
