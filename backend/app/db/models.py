"""SQLAlchemy ORM models for GeoStory database tables.

This module defines the ORM models that map to the database schema
created by Alembic migrations. Models match the schema defined in
docs/schema.sql and docs/schema.md.

Tables:
- users: User accounts (email nullable for anonymous support)
- stories: Location-based stories with geospatial data
- photos: Photo metadata for stories (images stored in GCS)
"""

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    Double,
    ForeignKey,
    Integer,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    """User account model.
    
    Represents a user who can create stories. Email is nullable to support
    anonymous story creation in the MVP phase.
    """
    
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    
    # User data
    email: Mapped[Optional[str]] = mapped_column(Text, unique=True, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    
    # Relationships
    stories: Mapped[List["Story"]] = relationship(
        "Story",
        back_populates="owner",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class Story(Base):
    """Story model.
    
    Represents a location-based story with title, body, category, and
    geographic coordinates. Stories can be anonymous (owner_id=NULL) or
    attributed to a user.
    """
    
    __tablename__ = "stories"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    
    # Foreign keys
    owner_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Story content
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(
        Text,
        CheckConstraint(
            "category IN ('travel', 'food', 'history', 'culture', 'nature', 'urban', 'personal')",
            name="stories_category_check",
        ),
        nullable=True,
    )
    
    # Geospatial data
    location_lat: Mapped[float] = mapped_column(
        Double,
        CheckConstraint(
            "location_lat >= -90 AND location_lat <= 90",
            name="stories_latitude_check",
        ),
        nullable=False,
    )
    location_lng: Mapped[float] = mapped_column(
        Double,
        CheckConstraint(
            "location_lng >= -180 AND location_lng <= 180",
            name="stories_longitude_check",
        ),
        nullable=False,
    )
    
    # Story metadata
    date_of_story: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    
    # Relationships
    owner: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="stories",
    )
    photos: Mapped[List["Photo"]] = relationship(
        "Photo",
        back_populates="story",
        order_by="Photo.ordinal",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<Story(id={self.id}, title={self.title!r})>"


class Photo(Base):
    """Photo model.
    
    Represents photo metadata for a story. Actual images are stored in
    Google Cloud Storage; this model stores the URL and metadata.
    Photos are ordered by the 'ordinal' field for gallery display.
    """
    
    __tablename__ = "photos"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    
    # Foreign keys
    story_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("stories.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    # Photo data
    gcs_url: Mapped[str] = mapped_column(Text, nullable=False)
    filename: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    caption: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    
    # Relationships
    story: Mapped["Story"] = relationship(
        "Story",
        back_populates="photos",
    )
    
    def __repr__(self) -> str:
        return f"<Photo(id={self.id}, story_id={self.story_id}, ordinal={self.ordinal})>"
