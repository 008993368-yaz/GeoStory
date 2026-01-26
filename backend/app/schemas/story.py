"""Pydantic schemas for Story model.

These schemas define the shape of Story data in API requests and responses.
"""

from datetime import date, datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.constants import StoryCategory
from .photo import PhotoRead


# Create a Literal type from the enum for Pydantic validation
StoryCategoryLiteral = Literal[
    StoryCategory.TRAVEL,
    StoryCategory.FOOD,
    StoryCategory.HISTORY,
    StoryCategory.CULTURE,
    StoryCategory.NATURE,
    StoryCategory.URBAN,
    StoryCategory.PERSONAL,
]


class StoryBase(BaseModel):
    """Base Story schema with common fields."""
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Story title",
    )
    body: Optional[str] = Field(
        None,
        max_length=50000,
        description="Story content (markdown-friendly, max 50k chars)",
    )
    category: Optional[StoryCategoryLiteral] = Field(
        None,
        description="Story category",
    )
    location_lat: float = Field(..., ge=-90, le=90, description="Latitude (WGS84)")
    location_lng: float = Field(..., ge=-180, le=180, description="Longitude (WGS84)")
    date_of_story: Optional[date] = Field(
        None,
        description="Date when the story occurred (must not be in the future)",
    )
    
    @field_validator('date_of_story')
    @classmethod
    def validate_date_not_future(cls, v: Optional[date]) -> Optional[date]:
        """Ensure date_of_story is not in the future."""
        if v is not None and v > date.today():
            raise ValueError('Story date cannot be in the future')
        return v


class StoryCreate(StoryBase):
    """Schema for creating a new story.
    
    Used when submitting a new story. owner_id is typically derived
    from the authenticated user context, not passed in the request body.
    """
    
    pass


class StoryRead(StoryBase):
    """Schema for reading story data from the database.
    
    This is the response model for story-related endpoints.
    Includes relationships like photos.
    """
    
    id: UUID
    owner_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    photos: List[PhotoRead] = Field(default_factory=list, description="Story photos")
    
    # Pydantic v2 config for ORM compatibility
    model_config = ConfigDict(from_attributes=True)


class StoryUpdate(BaseModel):
    """Schema for updating story data.
    
    All fields are optional for partial updates (PATCH semantics).
    """
    
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    body: Optional[str] = Field(None, max_length=50000)
    category: Optional[StoryCategoryLiteral] = None
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lng: Optional[float] = Field(None, ge=-180, le=180)
    date_of_story: Optional[date] = None
    
    @field_validator('date_of_story')
    @classmethod
    def validate_date_not_future(cls, v: Optional[date]) -> Optional[date]:
        """Ensure date_of_story is not in the future."""
        if v is not None and v > date.today():
            raise ValueError('Story date cannot be in the future')
        return v
    
    model_config = ConfigDict(from_attributes=True)


class StoryList(BaseModel):
    """Schema for paginated story lists.
    
    Used for timeline and filtered story endpoints.
    """
    
    stories: List[StoryRead]
    total: int
    page: int = 1
    page_size: int = 20
    
    model_config = ConfigDict(from_attributes=True)
