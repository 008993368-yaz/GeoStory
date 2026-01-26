"""Shared constants and enumerations for the GeoStory application.

This module provides centralized definitions for application-wide constants,
particularly for database constraints and validation.
"""

from enum import Enum


class StoryCategory(str, Enum):
    """Valid story categories.
    
    This enum serves as the single source of truth for story categories.
    It is used in:
    - Database CHECK constraints (Alembic migrations)
    - SQLAlchemy ORM models
    - Pydantic schema validation
    
    To add a new category:
    1. Add the value here
    2. Create an Alembic migration to update the DB constraint
    3. The ORM and schemas will automatically use the new value
    """
    
    TRAVEL = "travel"
    FOOD = "food"
    HISTORY = "history"
    CULTURE = "culture"
    NATURE = "nature"
    URBAN = "urban"
    PERSONAL = "personal"
    
    @classmethod
    def values(cls) -> list[str]:
        """Get all category values as a list of strings.
        
        Returns:
            List of all category values
        """
        return [category.value for category in cls]
    
    @classmethod
    def sql_check_constraint(cls) -> str:
        """Generate SQL CHECK constraint for database.
        
        Returns:
            SQL expression: category IN ('travel', 'food', ...)
        """
        values = "', '".join(cls.values())
        return f"category IN ('{values}')"
