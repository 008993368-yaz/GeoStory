"""SQLAlchemy declarative base for ORM models.

This module provides the base class for all SQLAlchemy ORM models.
Using SQLAlchemy 2.0 style declarative base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models.
    
    All database models should inherit from this class.
    This enables SQLAlchemy's declarative mapping system.
    """
    pass
