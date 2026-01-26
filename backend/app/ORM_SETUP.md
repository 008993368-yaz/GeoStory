# SQLAlchemy ORM Models & Database Setup - Implementation Guide

## What Was Implemented

This implementation adds SQLAlchemy ORM models, async database session management, and Pydantic schemas to the GeoStory backend.

### 📁 Project Structure

```
backend/app/
├── core/
│   ├── __init__.py
│   └── config.py              # Pydantic settings management
├── db/
│   ├── __init__.py
│   ├── base.py                # SQLAlchemy declarative base
│   ├── models.py              # ORM models (User, Story, Photo)
│   └── session.py             # Async engine and session factory
├── schemas/
│   ├── __init__.py
│   ├── user.py                # User Pydantic schemas
│   ├── story.py               # Story Pydantic schemas
│   └── photo.py               # Photo Pydantic schemas
├── deps.py                    # FastAPI dependencies (get_db)
└── main.py                    # FastAPI app (updated to use config)
```

### Updated Files

- ✅ `requirements.txt` - Added sqlalchemy>=2.0, asyncpg, greenlet, pydantic-settings
- ✅ `.env.example` - Added async DATABASE_URL format
- ✅ `app/main.py` - Updated to use centralized config

## Installation & Setup

### 1. Install New Dependencies

```bash
# Activate virtual environment first
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Install/update all dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Update your `.env` file with the **async** DATABASE_URL format:

```env
DATABASE_URL=postgresql+asyncpg://ls_user:password@localhost:5432/geostory
```

**Important:** 
- Application runtime uses `postgresql+asyncpg://` (async driver)
- Alembic migrations still use `postgresql://` (sync driver)
- The migration env.py handles this automatically

### 3. Verify Installation

Start the development server:

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Test the health endpoint:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status": "ok"}
```

## ORM Models

### User Model

```python
from app.db.models import User

# Fields:
# - id: UUID (primary key)
# - email: Optional[str] (unique, nullable for anonymous users)
# - created_at: datetime
# - stories: relationship to Story
```

### Story Model

```python
from app.db.models import Story

# Fields:
# - id: UUID (primary key)
# - owner_id: Optional[UUID] (FK to users, nullable)
# - title: str (required)
# - body: Optional[str]
# - category: Optional[str] (validated enum)
# - location_lat: float (-90 to 90)
# - location_lng: float (-180 to 180)
# - date_of_story: Optional[date]
# - created_at: datetime
# - updated_at: datetime
# - owner: relationship to User
# - photos: relationship to Photo (ordered by ordinal)
```

### Photo Model

```python
from app.db.models import Photo

# Fields:
# - id: UUID (primary key)
# - story_id: UUID (FK to stories, cascade delete)
# - gcs_url: str (required)
# - filename: Optional[str]
# - caption: Optional[str]
# - ordinal: int (default 0)
# - created_at: datetime
# - story: relationship to Story
```

## Using the Database Session

### In FastAPI Endpoints (Future)

```python
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db
from app.db.models import Story
from app.schemas.story import StoryRead

@app.get("/api/stories", response_model=list[StoryRead])
async def list_stories(db: AsyncSession = Depends(get_db)):
    """Get all stories."""
    result = await db.execute(select(Story))
    stories = result.scalars().all()
    return stories
```

### Direct Usage (Testing)

```python
from app.db.session import AsyncSessionLocal
from app.db.models import Story

async def test_query():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Story))
        stories = result.scalars().all()
        return stories
```

## Pydantic Schemas

### User Schemas

- `UserCreate` - For user registration (email optional)
- `UserRead` - API response model with id, email, created_at
- `UserUpdate` - For updating user data (all fields optional)

### Story Schemas

- `StoryCreate` - For creating stories (title, body, category, lat/lng, date)
- `StoryRead` - API response with all fields + photos relationship
- `StoryUpdate` - For updating stories (all fields optional)
- `StoryList` - Paginated response with total, page info

### Photo Schemas

- `PhotoCreate` - For uploading photos (gcs_url, filename, caption, ordinal)
- `PhotoRead` - API response with all fields
- `PhotoUpdate` - For updating photo metadata (all fields optional)

## Configuration

### Available Settings (app/core/config.py)

```python
from app.core.config import settings

# Access configuration
print(settings.DATABASE_URL)        # postgresql+asyncpg://...
print(settings.cors_origins_list)   # ['http://localhost:5173']
print(settings.DEBUG)                # True
print(settings.APP_ENV)              # 'development'
```

Settings are loaded from:
1. Environment variables
2. `.env` file
3. Default values

## Validation

### Models Match Alembic Schema

✅ **Table names:** users, stories, photos  
✅ **Column types:** UUID, Text, Double, Date, TIMESTAMPTZ  
✅ **Constraints:** lat/lng ranges, category enum, nullable fields  
✅ **Foreign keys:** owner_id → users.id (SET NULL), story_id → stories.id (CASCADE)  
✅ **Relationships:** User ↔ Story ↔ Photo with proper backpopulates  

### Pydantic Compatibility

✅ **ORM mode enabled:** `model_config = ConfigDict(from_attributes=True)`  
✅ **Field validation:** Min/max for lat/lng, regex for category  
✅ **Type safety:** UUID, datetime, Optional fields  
✅ **Nested models:** StoryRead includes List[PhotoRead]  

## Testing Checklist

- [ ] Dependencies installed: `pip list | grep -E "sqlalchemy|asyncpg|pydantic-settings"`
- [ ] Server starts without errors: `uvicorn app.main:app --reload`
- [ ] Health endpoint works: `curl http://localhost:8000/api/health`
- [ ] No import errors in Python shell:
  ```python
  from app.db.models import User, Story, Photo
  from app.schemas.story import StoryCreate, StoryRead
  from app.deps import get_db
  from app.core.config import settings
  ```
- [ ] Database migrations applied: `alembic current`
- [ ] Can create async session:
  ```python
  from app.db.session import AsyncSessionLocal
  async with AsyncSessionLocal() as db:
      print("Session created!")
  ```

## Common Issues & Solutions

### Import Error: "pydantic_settings not found"

```bash
pip install pydantic-settings
```

### Import Error: "asyncpg not found"

```bash
pip install asyncpg
```

### Database Connection Error

Check your `.env` file:
- Use `postgresql+asyncpg://` for APPLICATION
- Ensure database exists: `createdb geostory`
- Verify credentials and host/port

### "Target database is not up to date"

Run migrations:
```bash
alembic -c alembic.ini upgrade head
```

## Next Steps

1. ✅ ORM models and schemas are ready
2. ⏭️ Implement CRUD endpoints for stories (Epic 3)
3. ⏭️ Add authentication and user management
4. ⏭️ Implement photo upload to Google Cloud Storage
5. ⏭️ Add filtering and search endpoints

## Architecture Notes

- **Async all the way:** SQLAlchemy 2.0 async engine with asyncpg driver
- **Clean separation:** Models (ORM) vs Schemas (API contracts)
- **Type safety:** Full typing with Mapped[] and Pydantic models
- **Relationship loading:** `lazy="selectin"` for efficient async queries
- **Session management:** Context manager ensures proper cleanup
- **Configuration:** Centralized settings with environment variable support

## Documentation

- ORM Models: See inline documentation in [app/db/models.py](app/db/models.py)
- Database Schema: See [docs/schema.md](../../docs/schema.md)
- Pydantic Schemas: See inline documentation in [app/schemas/](app/schemas/)
- Configuration: See [app/core/config.py](app/core/config.py)
