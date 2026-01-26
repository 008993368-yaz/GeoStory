"""Pydantic schemas for Photo model.

These schemas define the shape of Photo data in API requests and responses.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class PhotoBase(BaseModel):
    """Base Photo schema with common fields."""
    
    gcs_url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Google Cloud Storage URL for the photo",
    )
    filename: Optional[str] = Field(
        None,
        max_length=255,
        description="Original filename",
    )
    caption: Optional[str] = Field(
        None,
        max_length=1000,
        description="Photo caption or alt text",
    )
    ordinal: int = Field(0, ge=0, description="Display order (0-indexed)")


class PhotoCreate(PhotoBase):
    """Schema for creating a new photo.
    
    Used when uploading photos to a story.
    story_id is typically provided via the URL path, not in the body.
    """
    
    pass


class PhotoRead(PhotoBase):
    """Schema for reading photo data from the database.
    
    This is the response model for photo-related endpoints.
    """
    
    id: UUID
    story_id: UUID
    created_at: datetime
    
    # Pydantic v2 config for ORM compatibility
    model_config = ConfigDict(from_attributes=True)


class PhotoUpdate(BaseModel):
    """Schema for updating photo data.
    
    All fields are optional for partial updates.
    """
    
    gcs_url: Optional[str] = Field(None, min_length=1, max_length=2048)
    filename: Optional[str] = Field(None, max_length=255)
    caption: Optional[str] = Field(None, max_length=1000)
    ordinal: Optional[int] = Field(None, ge=0)
    
    model_config = ConfigDict(from_attributes=True)
