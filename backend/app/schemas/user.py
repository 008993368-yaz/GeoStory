"""Pydantic schemas for User model.

These schemas define the shape of User data in API requests and responses.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Base User schema with common fields."""
    
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    """Schema for creating a new user.
    
    In the future, this will include password and other registration fields.
    For MVP, email is optional to support anonymous users.
    """
    
    pass


class UserRead(UserBase):
    """Schema for reading user data from the database.
    
    This is the response model for user-related endpoints.
    """
    
    id: UUID
    created_at: datetime
    
    # Pydantic v2 config for ORM compatibility
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Schema for updating user data.
    
    All fields are optional for partial updates.
    """
    
    email: Optional[EmailStr] = None
    
    model_config = ConfigDict(from_attributes=True)
