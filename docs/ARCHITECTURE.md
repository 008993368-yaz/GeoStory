# GeoStory Architecture

Technical design document for the GeoStory location-based storytelling platform.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT BROWSER                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                         React + TypeScript                               ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────────┐  ││
│  │  │   Home.tsx   │  │ StoryCreate  │  │      Shared Components        │  ││
│  │  │  - MapView   │  │  - Form      │  │  - StoryCard, AppLayout       │  ││
│  │  │  - StoryList │  │  - MapPicker │  │  - Calcite Design System      │  ││
│  │  └──────┬───────┘  └──────┬───────┘  └───────────────────────────────┘  ││
│  │         │                 │                                              ││
│  │         └────────┬────────┘                                              ││
│  │                  ▼                                                       ││
│  │         ┌───────────────────┐                                            ││
│  │         │  services/        │  Axios HTTP Client                         ││
│  │         │  - stories.ts     │  - listStories, createStory, getStory      ││
│  │         └─────────┬─────────┘                                            ││
│  └───────────────────┼──────────────────────────────────────────────────────┘│
└──────────────────────┼──────────────────────────────────────────────────────┘
                       │ HTTP/REST (JSON)
                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (FastAPI)                                   │
│  ┌──────────────────────────────────────────────────────────────────────────┐│
│  │                        app/main.py                                        ││
│  │   FastAPI App  →  CORS Middleware  →  Router Registration                 ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                │                                              │
│                                ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────────┐│
│  │                     routers/stories.py                                    ││
│  │   POST /api/stories     →  create_story()                                 ││
│  │   GET  /api/stories     →  list_stories()                                 ││
│  │   GET  /api/stories/:id →  get_story()                                    ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                │                                              │
│                                ▼                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌─────────────────────────┐ │
│  │  schemas/story.py  │  │  crud/stories.py   │  │   db/models.py          │ │
│  │  Pydantic Models   │  │  CRUD Operations   │  │   SQLAlchemy ORM        │ │
│  │  - StoryCreate     │  │  - create_story    │  │   - Story, User, Photo  │ │
│  │  - StoryResponse   │  │  - get_story       │  │                         │ │
│  │  - StoryListParams │  │  - list_stories    │  │                         │ │
│  └────────────────────┘  └─────────┬──────────┘  └────────────┬────────────┘ │
│                                    │                          │               │
│                                    └──────────┬───────────────┘               │
│                                               ▼                               │
│                               ┌───────────────────────────┐                   │
│                               │   db/session.py           │                   │
│                               │   AsyncSession Factory    │                   │
│                               │   - get_db() dependency   │                   │
│                               └─────────────┬─────────────┘                   │
└─────────────────────────────────────────────┼─────────────────────────────────┘
                                              │ asyncpg (async)
                                              ▼
                              ┌───────────────────────────────┐
                              │       PostgreSQL 15           │
                              │  ┌─────────────────────────┐  │
                              │  │  stories                │  │
                              │  │  - id, title, body      │  │
                              │  │  - location_lat/lng     │  │
                              │  │  - category, date       │  │
                              │  │  - created_at           │  │
                              │  └─────────────────────────┘  │
                              │  ┌─────────────────────────┐  │
                              │  │  users (future)         │  │
                              │  └─────────────────────────┘  │
                              │  ┌─────────────────────────┐  │
                              │  │  photos (future)        │  │
                              │  └─────────────────────────┘  │
                              └───────────────────────────────┘
```

---

## Data Flow

### Creating a Story

```
1. User fills StoryCreate form
   └─→ Form validation (client-side)
       └─→ User clicks map to set location
           └─→ LocationPickerMap.onChange() updates form state

2. User submits form
   └─→ stories.createStory(payload)
       └─→ POST /api/stories
           └─→ Pydantic validates StoryCreate schema
               └─→ crud.create_story() inserts row
                   └─→ Returns StoryResponse with ID

3. Frontend shows success
   └─→ Redirects to Home page
```

### Listing Stories with Filters

```
1. User opens Home page
   └─→ URL query params parsed (?category=personal&search=...)
       └─→ stories.listStories(params)
           └─→ GET /api/stories?category=personal&...

2. Backend processes request
   └─→ StoryListParams validates query params
       └─→ crud.list_stories() builds dynamic query
           └─→ Applies filters, sorting, pagination
               └─→ Returns StoryListResponse { items, total, limit, offset }

3. Frontend renders results
   └─→ MapView plots pins from stories array
   └─→ StoryList renders cards (grid or timeline mode)
   └─→ Bidirectional selection: click pin ↔ click card
```

---

## Key Modules

### Frontend

| Module | Purpose |
|--------|---------|
| `pages/Home.tsx` | Main page with map and story list, manages filter state via URL |
| `pages/StoryCreate.tsx` | Story creation form with validation |
| `components/map/MapView.tsx` | ArcGIS map with story pins, handles selection |
| `components/map/LocationPickerMap.tsx` | Click-to-select location for story creation |
| `components/story/StoryCard.tsx` | Story card with Calcite styling |
| `components/story/StoryList.tsx` | Grid/timeline list with view mode toggle |
| `services/stories.ts` | API client for story CRUD operations |
| `types/index.ts` | TypeScript interfaces for Story, filters, etc. |

### Backend

| Module | Purpose |
|--------|---------|
| `app/main.py` | FastAPI app initialization, CORS, router mounting |
| `routers/stories.py` | REST endpoints for stories |
| `crud/stories.py` | Database operations with async SQLAlchemy |
| `schemas/story.py` | Pydantic models for request/response validation |
| `db/models.py` | SQLAlchemy ORM models (Story, User, Photo) |
| `db/session.py` | Async session factory and dependency injection |
| `alembic/` | Database migration scripts |

---

## Technology Choices

### Why These Technologies?

| Choice | Rationale |
|--------|-----------|
| **React + TypeScript** | Type safety, excellent tooling, matches job requirements for modern frontend |
| **Calcite Design System** | Esri's official design system, consistent with ArcGIS ecosystem |
| **ArcGIS JS API** | Industry-standard GIS mapping, demonstrates geospatial expertise |
| **FastAPI** | Modern async Python framework, auto-generated OpenAPI docs |
| **Async SQLAlchemy** | Non-blocking DB access, modern Python async patterns |
| **PostgreSQL** | Robust RDBMS, native JSON support, PostGIS-ready for future geo queries |
| **Alembic** | Industry-standard migration tool, works seamlessly with SQLAlchemy |
| **Docker Compose** | Reproducible dev environment, easy onboarding |

### Key Technical Decisions

1. **URL-based State in Home Page**
   - Filter state stored in URL query params
   - Enables shareable links, browser back/forward navigation
   - State survives page refresh

2. **Async Database Access**
   - Uses `asyncpg` driver with `AsyncSession`
   - Non-blocking I/O for better concurrency
   - Requires careful transaction management

3. **Bidirectional Map Selection**
   - Map pins and list cards share selection state
   - Clicking either highlights both
   - Map pans to selected story location

---

## Database Schema

```sql
-- Core stories table
CREATE TABLE stories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    body TEXT,
    category VARCHAR(50) CHECK (category IN ('personal', 'historical', ...)),
    location_lat NUMERIC(9,6) NOT NULL CHECK (location_lat BETWEEN -90 AND 90),
    location_lng NUMERIC(10,6) NOT NULL CHECK (location_lng BETWEEN -180 AND 180),
    date_of_story DATE,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_stories_category ON stories(category);
CREATE INDEX idx_stories_created_at ON stories(created_at DESC);
CREATE INDEX idx_stories_date_of_story ON stories(date_of_story DESC);
```

See [docs/schema.md](schema.md) for complete schema documentation.

---

## Testing Strategy

### Backend Testing

- **Framework**: pytest with pytest-asyncio
- **Database**: Isolated test database via docker-compose.test.yml
- **Isolation**: Per-test transactions that rollback
- **Coverage**: 100 tests covering CRUD, validation, edge cases

```python
# Example: Testing story creation
async def test_create_story_success(db_session):
    story = await crud.create_story(db_session, StoryCreate(...))
    assert story.id is not None
    assert story.title == "Test Story"
```

### Frontend Testing

- **Framework**: Vitest with @testing-library/react
- **Environment**: jsdom with Calcite custom element stubs
- **Mocking**: vi.mock for API services and map components
- **Coverage**: Smoke tests for key pages (Home, StoryCreate)

```typescript
// Example: Testing page renders
it('renders story cards when API returns stories', async () => {
  mockListStories.mockResolvedValue({ items: [mockStory], total: 1 });
  renderWithRouter(<Home />);
  await waitFor(() => {
    expect(screen.getByText('Test Story')).toBeInTheDocument();
  });
});
```

---

## Future Roadmap

### Phase 1: Photo Uploads
- Google Cloud Storage integration
- Presigned URL generation for direct uploads
- Photo gallery component on story detail page

### Phase 2: Authentication
- OAuth2 with JWT tokens
- User profile management
- Story ownership and edit permissions

### Phase 3: Production Deployment
- Nginx reverse proxy with SSL
- Cloud Run or Kubernetes deployment
- CI/CD pipeline with GitHub Actions

### Phase 4: Advanced Features
- Map clustering for performance with many pins
- Spatial queries with PostGIS
- Real-time updates with WebSockets
