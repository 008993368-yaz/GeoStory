"""Pydantic schemas for Photo model.

These schemas define the shape of Photo data in API requests and responses.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PhotoBase(BaseModel):
    """Base Photo schema with common fields."""
    
    gcs_url: str = Field(..., description="Google Cloud Storage URL for the photo")
    filename: Optional[str] = Field(None, description="Original filename")
    caption: Optional[str] = Field(None, description="Photo caption or alt text")
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
    
    gcs_url: Optional[str] = None
    filename: Optional[str] = None
    caption: Optional[str] = None
    ordinal: Optional[int] = Field(None, ge=0)
    
    model_config = ConfigDict(from_attributes=True)
