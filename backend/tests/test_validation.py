"""Unit tests for validation consistency across Story and Photo schemas.

Tests ensure that Pydantic validation catches invalid data before it reaches
the database layer, providing better error messages and faster failure.
"""

import pytest
from datetime import date, timedelta
from pydantic import ValidationError

from app.schemas.story import StoryCreate, StoryUpdate
from app.schemas.photo import PhotoCreate, PhotoUpdate


class TestStoryTitleValidation:
    """Test suite for story title validation."""
    
    def test_title_required(self):
        """Test that title is required."""
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                location_lat=40.7128,
                location_lng=-74.0060,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("title",)
        assert "Field required" in error["msg"]
    
    def test_title_empty_string_rejected(self):
        """Test that empty title is rejected (min_length=1)."""
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="",
                location_lat=40.7128,
                location_lng=-74.0060,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("title",)
        assert "at least 1 character" in error["msg"]
    
    def test_title_max_length_enforced(self):
        """Test that title exceeding 500 chars is rejected."""
        long_title = "A" * 501
        
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title=long_title,
                location_lat=40.7128,
                location_lng=-74.0060,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("title",)
        assert "at most 500 characters" in error["msg"]
    
    def test_title_exactly_500_chars_accepted(self):
        """Test that title with exactly 500 chars is accepted."""
        title_500 = "A" * 500
        
        story = StoryCreate(
            title=title_500,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert len(story.title) == 500
    
    def test_title_normal_length_accepted(self):
        """Test that normal title is accepted."""
        story = StoryCreate(
            title="Golden Gate Bridge at Sunset",
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.title == "Golden Gate Bridge at Sunset"


class TestStoryBodyValidation:
    """Test suite for story body validation."""
    
    def test_body_optional(self):
        """Test that body is optional."""
        story = StoryCreate(
            title="Test Story",
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.body is None
    
    def test_body_none_accepted(self):
        """Test that body=None is accepted."""
        story = StoryCreate(
            title="Test Story",
            body=None,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.body is None
    
    def test_body_empty_string_accepted(self):
        """Test that empty string body is accepted."""
        story = StoryCreate(
            title="Test Story",
            body="",
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.body == ""
    
    def test_body_max_length_enforced(self):
        """Test that body exceeding 50k chars is rejected."""
        long_body = "A" * 50001
        
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="Test Story",
                body=long_body,
                location_lat=40.7128,
                location_lng=-74.0060,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("body",)
        assert "at most 50000 characters" in error["msg"]
    
    def test_body_exactly_50k_chars_accepted(self):
        """Test that body with exactly 50k chars is accepted."""
        body_50k = "A" * 50000
        
        story = StoryCreate(
            title="Test Story",
            body=body_50k,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert len(story.body) == 50000
    
    def test_body_normal_text_accepted(self):
        """Test that normal body text is accepted."""
        story = StoryCreate(
            title="Test Story",
            body="This is a beautiful story about my travels.",
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.body == "This is a beautiful story about my travels."


class TestLocationValidation:
    """Test suite for lat/lng validation."""
    
    def test_latitude_below_minus_90_rejected(self):
        """Test that latitude < -90 is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="Test Story",
                location_lat=-90.1,
                location_lng=0,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("location_lat",)
        assert "greater than or equal to -90" in error["msg"]
    
    def test_latitude_above_90_rejected(self):
        """Test that latitude > 90 is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="Test Story",
                location_lat=90.1,
                location_lng=0,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("location_lat",)
        assert "less than or equal to 90" in error["msg"]
    
    def test_latitude_exactly_minus_90_accepted(self):
        """Test that latitude = -90 is accepted (South Pole)."""
        story = StoryCreate(
            title="South Pole",
            location_lat=-90.0,
            location_lng=0,
        )
        assert story.location_lat == -90.0
    
    def test_latitude_exactly_90_accepted(self):
        """Test that latitude = 90 is accepted (North Pole)."""
        story = StoryCreate(
            title="North Pole",
            location_lat=90.0,
            location_lng=0,
        )
        assert story.location_lat == 90.0
    
    def test_longitude_below_minus_180_rejected(self):
        """Test that longitude < -180 is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="Test Story",
                location_lat=0,
                location_lng=-180.1,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("location_lng",)
        assert "greater than or equal to -180" in error["msg"]
    
    def test_longitude_above_180_rejected(self):
        """Test that longitude > 180 is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="Test Story",
                location_lat=0,
                location_lng=180.1,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("location_lng",)
        assert "less than or equal to 180" in error["msg"]
    
    def test_longitude_exactly_minus_180_accepted(self):
        """Test that longitude = -180 is accepted."""
        story = StoryCreate(
            title="Dateline West",
            location_lat=0,
            location_lng=-180.0,
        )
        assert story.location_lng == -180.0
    
    def test_longitude_exactly_180_accepted(self):
        """Test that longitude = 180 is accepted."""
        story = StoryCreate(
            title="Dateline East",
            location_lat=0,
            location_lng=180.0,
        )
        assert story.location_lng == 180.0
    
    def test_valid_location_accepted(self):
        """Test that valid lat/lng is accepted."""
        story = StoryCreate(
            title="New York City",
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.location_lat == 40.7128
        assert story.location_lng == -74.0060


class TestDateOfStoryValidation:
    """Test suite for date_of_story validation."""
    
    def test_date_optional(self):
        """Test that date_of_story is optional."""
        story = StoryCreate(
            title="Test Story",
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.date_of_story is None
    
    def test_date_none_accepted(self):
        """Test that date_of_story=None is accepted."""
        story = StoryCreate(
            title="Test Story",
            date_of_story=None,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.date_of_story is None
    
    def test_past_date_accepted(self):
        """Test that past dates are accepted."""
        past_date = date(2020, 1, 1)
        
        story = StoryCreate(
            title="Old Story",
            date_of_story=past_date,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.date_of_story == past_date
    
    def test_today_accepted(self):
        """Test that today's date is accepted."""
        today = date.today()
        
        story = StoryCreate(
            title="Today's Story",
            date_of_story=today,
            location_lat=40.7128,
            location_lng=-74.0060,
        )
        assert story.date_of_story == today
    
    def test_future_date_rejected(self):
        """Test that future dates are rejected."""
        tomorrow = date.today() + timedelta(days=1)
        
        with pytest.raises(ValidationError) as exc_info:
            StoryCreate(
                title="Future Story",
                date_of_story=tomorrow,
                location_lat=40.7128,
                location_lng=-74.0060,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("date_of_story",)
        assert "cannot be in the future" in str(error["msg"])


class TestStoryUpdateValidation:
    """Test suite for StoryUpdate validation."""
    
    def test_update_all_fields_optional(self):
        """Test that all fields are optional in update."""
        update = StoryUpdate()
        assert update.title is None
        assert update.body is None
        assert update.category is None
    
    def test_update_title_length_enforced(self):
        """Test that title length is enforced in updates."""
        with pytest.raises(ValidationError):
            StoryUpdate(title="A" * 501)
    
    def test_update_body_length_enforced(self):
        """Test that body length is enforced in updates."""
        with pytest.raises(ValidationError):
            StoryUpdate(body="A" * 50001)
    
    def test_update_future_date_rejected(self):
        """Test that future dates are rejected in updates."""
        tomorrow = date.today() + timedelta(days=1)
        
        with pytest.raises(ValidationError):
            StoryUpdate(date_of_story=tomorrow)
    
    def test_update_partial_valid(self):
        """Test that partial updates are valid."""
        update = StoryUpdate(title="New Title")
        assert update.title == "New Title"
        assert update.body is None


class TestPhotoValidation:
    """Test suite for Photo schema validation."""
    
    def test_gcs_url_required(self):
        """Test that gcs_url is required."""
        with pytest.raises(ValidationError) as exc_info:
            PhotoCreate()
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("gcs_url",)
    
    def test_gcs_url_empty_rejected(self):
        """Test that empty gcs_url is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PhotoCreate(gcs_url="")
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("gcs_url",)
        assert "at least 1 character" in error["msg"]
    
    def test_gcs_url_max_length_enforced(self):
        """Test that gcs_url exceeding 2048 chars is rejected."""
        long_url = "https://storage.googleapis.com/" + ("A" * 2020)
        
        with pytest.raises(ValidationError) as exc_info:
            PhotoCreate(gcs_url=long_url)
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("gcs_url",)
        assert "at most 2048 characters" in error["msg"]
    
    def test_gcs_url_valid(self):
        """Test that valid URL is accepted."""
        photo = PhotoCreate(
            gcs_url="https://storage.googleapis.com/bucket/image.jpg"
        )
        assert photo.gcs_url == "https://storage.googleapis.com/bucket/image.jpg"
    
    def test_filename_optional(self):
        """Test that filename is optional."""
        photo = PhotoCreate(
            gcs_url="https://storage.googleapis.com/bucket/image.jpg"
        )
        assert photo.filename is None
    
    def test_filename_max_length_enforced(self):
        """Test that filename exceeding 255 chars is rejected."""
        long_filename = "A" * 256
        
        with pytest.raises(ValidationError) as exc_info:
            PhotoCreate(
                gcs_url="https://storage.googleapis.com/bucket/image.jpg",
                filename=long_filename,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("filename",)
        assert "at most 255 characters" in error["msg"]
    
    def test_caption_optional(self):
        """Test that caption is optional."""
        photo = PhotoCreate(
            gcs_url="https://storage.googleapis.com/bucket/image.jpg"
        )
        assert photo.caption is None
    
    def test_caption_max_length_enforced(self):
        """Test that caption exceeding 1000 chars is rejected."""
        long_caption = "A" * 1001
        
        with pytest.raises(ValidationError) as exc_info:
            PhotoCreate(
                gcs_url="https://storage.googleapis.com/bucket/image.jpg",
                caption=long_caption,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("caption",)
        assert "at most 1000 characters" in error["msg"]
    
    def test_ordinal_default_zero(self):
        """Test that ordinal defaults to 0."""
        photo = PhotoCreate(
            gcs_url="https://storage.googleapis.com/bucket/image.jpg"
        )
        assert photo.ordinal == 0
    
    def test_ordinal_negative_rejected(self):
        """Test that negative ordinal is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            PhotoCreate(
                gcs_url="https://storage.googleapis.com/bucket/image.jpg",
                ordinal=-1,
            )
        
        error = exc_info.value.errors()[0]
        assert error["loc"] == ("ordinal",)
        assert "greater than or equal to 0" in error["msg"]
    
    def test_ordinal_positive_accepted(self):
        """Test that positive ordinal is accepted."""
        photo = PhotoCreate(
            gcs_url="https://storage.googleapis.com/bucket/image.jpg",
            ordinal=5,
        )
        assert photo.ordinal == 5


class TestCompleteStoryValidation:
    """Integration tests for complete story creation."""
    
    def test_minimal_valid_story(self):
        """Test creating story with minimal required fields."""
        story = StoryCreate(
            title="Test",
            location_lat=0,
            location_lng=0,
        )
        assert story.title == "Test"
        assert story.body is None
        assert story.category is None
    
    def test_complete_valid_story(self):
        """Test creating story with all fields."""
        story = StoryCreate(
            title="Golden Gate Bridge",
            body="Beautiful sunset over the bay.",
            category="travel",
            location_lat=37.8199,
            location_lng=-122.4783,
            date_of_story=date(2026, 1, 25),
        )
        assert story.title == "Golden Gate Bridge"
        assert story.body == "Beautiful sunset over the bay."
        assert story.category == "travel"
        assert story.location_lat == 37.8199
        assert story.location_lng == -122.4783
        assert story.date_of_story == date(2026, 1, 25)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
