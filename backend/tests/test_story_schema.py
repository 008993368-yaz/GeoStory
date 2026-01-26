"""Unit tests for Story schema validation.

Tests ensure that category validation works correctly at the Pydantic layer,
matching the database constraints.
"""

import pytest
from datetime import date
from pydantic import ValidationError

from app.schemas.story import StoryCreate, StoryUpdate
from app.constants import StoryCategory


class TestStoryCategoryValidation:
    """Test suite for story category validation."""
    
    def test_valid_categories_accepted(self):
        """Test that all valid categories are accepted."""
        valid_categories = [
            "travel", "food", "history", "culture", 
            "nature", "urban", "personal"
        ]
        
        for category in valid_categories:
            story = StoryCreate(
                title="Test Story",
                category=category,
                location_lat=40.7128,
                location_lng=-74.0060,
            )
            assert story.category == category
    
    def test_enum_values_accepted(self):
        """Test that StoryCategory enum values work."""
        story = StoryCreate(
            title="Test Story",
            category=StoryCategory.TRAVEL.value,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.category == "travel"
    
    def test_invalid_category_rejected(self):
        """Test that invalid categories are rejected with clear error."""
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="Test Story",
                category="invalid_category",  # Not in allowed list
                location_lat=40.7128,
                location_lng=-74.0060,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("category",)
        assert "Input should be" in error["msg"]
    
    def test_category_case_sensitive(self):
        """Test that category validation is case-sensitive."""
        with pytest.raises(ValidationError):
            StoryCreate(
                title="Test Story",
                category="Travel",  # Capital T should fail
                location_lat=40.7128,
                location_lng=-74.0060,
            )
    
    def test_category_optional_none_allowed(self):
        """Test that category can be None (optional field)."""
        story = StoryCreate(
            title="Test Story",
            category=None,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.category is None
    
    def test_category_optional_omitted_allowed(self):
        """Test that category can be omitted entirely."""
        story = StoryCreate(
            title="Test Story",
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.category is None
    
    def test_story_update_valid_category(self):
        """Test that StoryUpdate accepts valid categories."""
        update = StoryUpdate(category="food")
        assert update.category == "food"
    
    def test_story_update_invalid_category(self):
        """Test that StoryUpdate rejects invalid categories."""
        with pytest.raises(ValidationError):
            StoryUpdate(category="sports")
    
    def test_story_update_none_category(self):
        """Test that StoryUpdate can set category to None."""
        update = StoryUpdate(category=None)
        assert update.category is None
    
    def test_story_update_partial(self):
        """Test that StoryUpdate works with only category changed."""
        update = StoryUpdate(category="nature")
        assert update.category == "nature"
        assert update.title is None
        assert update.body is None
    
    def test_complete_story_with_category(self):
        """Test creating a complete story with all fields including category."""
        story = StoryCreate(
            title="Golden Gate Bridge at Sunset",
            body="Amazing view of the sunset over the bay.",
            category="travel",
            location_lat=37.8199,
            location_lng=-122.4783,
            date_of_story=date(2026, 1, 25),
        )
        
        assert story.title == "Golden Gate Bridge at Sunset"
        assert story.category == "travel"
        assert story.location_lat == 37.8199
    
    def test_story_category_whitespace_rejected(self):
        """Test that category with whitespace is rejected."""
        with pytest.raises(ValidationError):
            StoryCreate(
                title="Test Story",
                category=" travel ",  # Whitespace should fail
                location_lat=40.7128,
                location_lng=-74.0060,
            )
    
    def test_story_category_empty_string_rejected(self):
        """Test that empty string category is rejected."""
        with pytest.raises(ValidationError):
            StoryCreate(
                title="Test Story",
                category="",  # Empty string should fail
                location_lat=40.7128,
                location_lng=-74.0060,
            )


class TestStoryCategoryConstants:
    """Test suite for StoryCategory enum."""
    
    def test_all_enum_values_exist(self):
        """Test that all expected categories exist in enum."""
        expected = {
            "travel", "food", "history", "culture",
            "nature", "urban", "personal"
        }
        actual = set(StoryCategory.values())
        assert actual == expected
    
    def test_sql_check_constraint_generation(self):
        """Test that SQL CHECK constraint is generated correctly."""
        constraint = StoryCategory.sql_check_constraint()
        
        # Should contain category IN (...)
        assert "category IN (" in constraint
        
        # Should contain all values
        for category in StoryCategory.values():
            assert f"'{category}'" in constraint
    
    def test_enum_value_access(self):
        """Test that enum values can be accessed properly."""
        assert StoryCategory.TRAVEL.value == "travel"
        assert StoryCategory.FOOD.value == "food"
        assert StoryCategory.HISTORY.value == "history"
        assert StoryCategory.CULTURE.value == "culture"
        assert StoryCategory.NATURE.value == "nature"
        assert StoryCategory.URBAN.value == "urban"
        assert StoryCategory.PERSONAL.value == "personal"
    
    def test_enum_iteration(self):
        """Test that enum can be iterated."""
        categories = list(StoryCategory)
        assert len(categories) == 7
        assert StoryCategory.TRAVEL in categories


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
